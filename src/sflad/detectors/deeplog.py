"""DeepLog-style source-free detector.

An LSTM predicts the next log key from the previous ``history`` keys, trained only on the training
part of the certified fault-free window. The separate, later calibration part sets ``g``: the smallest
g for which at most ``calib_fpr`` of its windows alarm. An event is anomalous if its key is unknown or
not in the top-``g`` predictions; a window is anomalous if any of its events is. A calibration window
with an unknown key alarms whatever g is, so it counts against the same allowance.
"""

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import numpy as np
import torch
from torch import nn

from sflad.data.schema import LogEvent
from sflad.detectors.base import (
    UNK_TOKEN,
    BaseDetector,
    DetectionResult,
    map_template_ids,
    prepare_events,
    training_and_calibration_events,
    window_end_indices,
    window_labels,
)
from sflad.parsing.template_parser import assign_templates


def _history_pairs(seq: np.ndarray, history: int) -> Tuple[np.ndarray, np.ndarray]:
    idx = np.arange(history, len(seq))
    if not len(idx):
        return np.zeros((0, history), dtype=np.int64), np.zeros(0, dtype=np.int64)
    return np.stack([seq[i - history : i] for i in idx]).astype(np.int64), seq[history:].astype(np.int64)


class NextKey(nn.Module):
    """Embeds the previous log keys, reads them with an LSTM and scores every key as the next one."""

    def __init__(self, n_keys: int, embed_dim: int, hidden: int, layers: int) -> None:
        super().__init__()
        self.emb = nn.Embedding(n_keys, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden, num_layers=layers, batch_first=True)
        self.out = nn.Linear(hidden, n_keys)

    def forward(self, x):
        h, _ = self.lstm(self.emb(x))
        return self.out(h[:, -1, :])


class DeepLogDetector(BaseDetector):
    name = "source_free_deeplog"

    def __init__(
        self,
        history: int = 10,
        hidden: int = 64,
        layers: int = 2,
        embed_dim: int = 32,
        epochs: int = 30,
        lr: float = 1e-3,
        batch_size: int = 64,
        calib_fpr: float = 0.01,
        calib_share: float = 0.5,
        train_share: float = 1.0,
        window_size: int = 20,
        step_size: int = 20,
        random_state: int = 42,
    ) -> None:
        self.history = history
        self.hidden = hidden
        self.layers = layers
        self.embed_dim = embed_dim
        self.epochs = epochs
        self.lr = lr
        self.batch_size = batch_size
        self.calib_fpr = calib_fpr
        self.calib_share = calib_share
        self.train_share = train_share
        self.window_size = window_size
        self.step_size = step_size
        self.random_state = random_state
        self.model = None
        self.vocab: Optional[dict] = None
        self.g: Optional[int] = None
        self.n_calib_windows = None
        self.n_train_events = None
        self._parser = None

    def _ranks(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Rank (1 = most likely) of the true next key under the model."""

        with torch.no_grad():
            logits = self.model(torch.from_numpy(X))
        logits[:, self.vocab[UNK_TOKEN]] = float("-inf")  # the unseen-key output is never trained
        true = logits.gather(1, torch.from_numpy(y).view(-1, 1))
        return (logits > true).sum(dim=1).numpy() + 1

    def _event_flags(self, seq: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Per event: unknown key, and rank of the true next key (0 for the first ``history`` events)."""
        unknown = (seq == self.vocab[UNK_TOKEN]).astype(int)
        ranks = np.zeros(len(seq), dtype=np.int64)
        X, y = _history_pairs(seq, self.history)
        if len(X):
            ranks[self.history :] = self._ranks(X, y)
        return unknown, ranks

    def _calibrate_g(self, seq: np.ndarray) -> int:
        """Smallest g at which at most calib_fpr of the calibration windows alarm."""
        unknown, ranks = self._event_flags(seq)
        ends = window_end_indices(len(seq), self.window_size, self.step_size)
        spans = [slice(max(0, int(e) - self.window_size + 1), int(e) + 1) for e in ends]
        forced = np.array([unknown[sp].any() for sp in spans])
        worst = np.array([ranks[sp][unknown[sp] == 0].max(initial=0) for sp in spans])
        self.n_calib_windows = len(spans)
        allowed = int(self.calib_fpr * len(spans)) - int(forced.sum())
        free = np.sort(worst[~forced])[::-1]
        if allowed < 0 or not len(free) or allowed >= len(free):
            # No further window may alarm (or none can): g is the largest rank seen.
            return int(max(free.max(initial=0), 1))
        return int(max(free[allowed], 1))

    def fit(self, events: Sequence[LogEvent], **kwargs) -> "DeepLogDetector":
        train, calib = training_and_calibration_events(events, self.calib_share, self.train_share)
        tids, _, self._parser = prepare_events(train)
        self.vocab = {t: i for i, t in enumerate(sorted(set(tids)))}
        self.vocab[UNK_TOKEN] = len(self.vocab)
        seq = np.array([self.vocab[t] for t in tids], dtype=np.int64)
        if len(seq) <= self.history:
            raise ValueError(f"the training part has {len(seq)} events; it must be longer than history={self.history}")
        if len(calib) < self.window_size:
            raise ValueError(f"the calibration part has {len(calib)} events; it needs a full window of {self.window_size}")
        self.n_train_events = int(len(seq))
        X, y = _history_pairs(seq, self.history)
        threads = torch.get_num_threads()
        try:
            with torch.random.fork_rng(devices=[]):
                torch.manual_seed(self.random_state)
                torch.set_num_threads(1)
                self.model = NextKey(len(self.vocab), self.embed_dim, self.hidden, self.layers)
                opt = torch.optim.Adam(self.model.parameters(), lr=self.lr)
                loss_fn = torch.nn.CrossEntropyLoss()
                Xt, yt = torch.from_numpy(X), torch.from_numpy(y)
                gen = torch.Generator().manual_seed(self.random_state)
                self.model.train()
                for _ in range(self.epochs):
                    for batch in torch.randperm(len(Xt), generator=gen).split(self.batch_size):
                        opt.zero_grad()
                        loss_fn(self.model(Xt[batch]), yt[batch]).backward()
                        opt.step()
        finally:
            torch.set_num_threads(threads)
        self.model.eval()
        self.g = self._calibrate_g(self._keys(calib))
        return self

    def _keys(self, events: Sequence[LogEvent]) -> np.ndarray:
        tids, _ = assign_templates([e.message for e in events], parser=self._parser)
        return np.array([self.vocab[t] for t in map_template_ids(tids, self.vocab)], dtype=np.int64)

    def predict(self, events: Sequence[LogEvent], **kwargs) -> DetectionResult:
        if self.model is None or self.vocab is None:
            raise RuntimeError("DeepLogDetector must be fit before predict")
        eval_events = [e for e in events if e.split == "eval"]
        if not eval_events:
            raise ValueError("no evaluation events (split == 'eval') to score")
        seq = self._keys(eval_events)
        unknown, ranks = self._event_flags(seq)
        flags = unknown | (ranks > self.g).astype(int)
        ends = window_end_indices(len(seq), self.window_size, self.step_size)
        per_window = [flags[max(0, int(e) - self.window_size + 1) : int(e) + 1] for e in ends]
        y_pred = np.array([int(w.any()) for w in per_window], dtype=int)
        scores = np.array([float(w.mean()) for w in per_window])
        y_true = window_labels(eval_events, ends, self.window_size)
        return DetectionResult(
            name=self.name,
            y_true=y_true,
            y_pred=y_pred,
            scores=scores,
            event_indices=ends,
            meta={
                "algorithm": "deeplog_lstm",
                "top_g": int(self.g),
                "calib_fpr": self.calib_fpr,
                "history": self.history,
                "n_keys": len(self.vocab),
                "n_calib_windows": self.n_calib_windows,
                "n_train_events": self.n_train_events,
                "n_windows": int(len(y_pred)),
            },
        )
