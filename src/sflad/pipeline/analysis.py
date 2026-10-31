"""Analysis of one application's pooled evaluation runs.

Windows of every evaluation run are pooled. Forfeiture F1(baseline) - F1(source-free detector) gets a
run-stratified bootstrap interval and an exact McNemar test. H1: against the BGL-trained baseline;
H2: against the OpenStack-trained baseline; H3: against the similar-application baseline; H4: recall
differs across fault categories (chi-square); H5: elasticity-window false alarms differ across the
primary detectors (Cochran's Q); H6: the similar-application and BGL-trained baselines differ. Both
source-free detectors get H1 to H4; H5 and H6 are tested once. All of them form one Holm-Bonferroni
family per application. H1 to H3 also carry a McNemar test on fault segments, outside that family.

Non-inferiority (the viability rule): a source-free detector is non-inferior to a baseline when the
upper one-sided 95% bootstrap bound of the forfeiture is below the margin; it is a viable substitute
when it is also above the threshold alarms' F1. Supplementary: the novelty gate's contribution, the
feature-space ablation, false alarms on elasticity windows with and without a new execution
environment, and recall per delay of the latency fault. Every run must have been scored with the same
configuration.

Usage: python -m sflad.pipeline.analysis OUT_DIR RUN_DIR [RUN_DIR ...]
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
from scipy import stats

from sflad.pipeline.metrics import FAULT_CATEGORIES, delay_summary, precision_recall_f1, segment_delays, segment_hits
from sflad.pipeline.train_eval import BASELINE_ARMS, SOURCE_FREE_ARMS, load_config

PRIMARY_ARMS = SOURCE_FREE_ARMS + BASELINE_ARMS + ("threshold",)
HYPOTHESIS_BASELINES = (("H1", "transfer"), ("H2", "transfer_openstack"), ("H3", "transfer_similar"))


def load_runs(run_dirs: Sequence[Path]) -> List[Dict[str, Any]]:
    runs = []
    for rd in run_dirs:
        w = json.loads((rd / "processed" / "window_predictions.json").read_text())
        res = json.loads((rd / "processed" / "results.json").read_text())
        y_true = np.asarray(w["y_true"], dtype=int)
        y_pred = {arm: np.asarray(p, dtype=int) for arm, p in w["y_pred"].items()}
        runs.append({
            "run": f"{rd.parent.name}/{rd.name}",
            "y_true": y_true,
            "categories": np.asarray(w["window_categories"], dtype=object),
            "control": np.asarray(w["control_windows"], dtype=bool),
            "cold_start": np.asarray(w["cold_start_windows"], dtype=bool),
            "strengths": np.asarray([s or 0 for s in w["window_strengths_ms"]], dtype=int),
            "y_pred": y_pred,
            "segment_hits": {arm: segment_hits(y_true, p) for arm, p in y_pred.items()},
            "segment_delays": {arm: segment_delays(y_true, p, w["window_end_ms"]) for arm, p in y_pred.items()},
            "config": res["config"],
        })
    return runs


def _f1(y_true: np.ndarray, y_pred: np.ndarray, weight: np.ndarray) -> float:
    tp = float(np.sum(weight * (y_true & y_pred)))
    fp = float(np.sum(weight * (~y_true & y_pred)))
    fn = float(np.sum(weight * (y_true & ~y_pred)))
    return 2 * tp / (2 * tp + fp + fn) if tp + fn else float("nan")


def bootstrap_f1_gap(runs, a: str, b: str, samples: int, rng: np.random.Generator) -> Dict[str, float]:
    """F1(a) - F1(b) on the pooled windows, with a 95% interval from resampling windows within each evaluation run."""
    y = np.concatenate([r["y_true"] for r in runs]).astype(bool)
    pa = np.concatenate([r["y_pred"][a] for r in runs]).astype(bool)
    pb = np.concatenate([r["y_pred"][b] for r in runs]).astype(bool)
    point = _f1(y, pa, np.ones(len(y))) - _f1(y, pb, np.ones(len(y)))
    sizes = [len(r["y_true"]) for r in runs]
    gaps = np.empty(samples)
    for s in range(samples):
        weight = np.concatenate([np.bincount(rng.integers(0, n, n), minlength=n) for n in sizes]).astype(float)
        gaps[s] = _f1(y, pa, weight) - _f1(y, pb, weight)
    undefined = int(np.isnan(gaps).sum())
    lo, hi, upper = np.nanpercentile(gaps, [2.5, 97.5, 95.0])
    return {"gap": float(point), "ci_low": float(lo), "ci_high": float(hi), "upper_one_sided_95": float(upper),
            "n_undefined_resamples": undefined}


def mcnemar(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> Dict[str, float]:
    """Exact McNemar test on paired window outcomes (each detector right or wrong on each window)."""
    right_a, right_b = pred_a == y_true, pred_b == y_true
    only_a, only_b = int(np.sum(right_a & ~right_b)), int(np.sum(~right_a & right_b))
    p = stats.binomtest(only_a, only_a + only_b, 0.5).pvalue if only_a + only_b else float("nan")
    return {"only_first_right": only_a, "only_second_right": only_b, "p": float(p)}


def category_recall_test(y_true: np.ndarray, y_pred: np.ndarray, categories: np.ndarray) -> Dict[str, Any]:
    """Chi-square test that recall is the same in every fault category with positive windows."""
    table, recall = [], {}
    for cat in FAULT_CATEGORIES:
        pos = (categories == cat) & (y_true == 1)
        if pos.any():
            hit = int(np.sum(y_pred[pos] == 1))
            table.append([hit, int(pos.sum()) - hit])
            recall[cat] = hit / int(pos.sum())
    if len(table) < 2 or all(row[1] == 0 for row in table) or all(row[0] == 0 for row in table):
        return {"recall": recall, "p": float("nan")}
    chi2, p, _, _ = stats.chi2_contingency(np.asarray(table))
    return {"recall": recall, "chi2": float(chi2), "p": float(p)}


def cochran_q(alarms: np.ndarray) -> Dict[str, float]:
    """Cochran's Q on a windows x detectors 0/1 matrix: do the detectors alarm at different rates?"""
    x = np.asarray(alarms, dtype=int)
    k = x.shape[1]
    col, row = x.sum(axis=0), x.sum(axis=1)
    denom = k * row.sum() - np.sum(row ** 2)
    informative = int(np.sum((row > 0) & (row < k)))  # windows on which the detectors disagree
    if x.shape[0] == 0 or denom == 0:
        return {"q": float("nan"), "p": float("nan"), "n_informative_windows": informative}
    q = (k - 1) * (k * np.sum(col ** 2) - row.sum() ** 2) / denom
    return {"q": float(q), "p": float(stats.chi2.sf(q, k - 1)), "n_informative_windows": informative}


def holm(pvalues: Dict[str, float], alpha: float) -> Dict[str, Dict[str, Any]]:
    """Holm-Bonferroni over the tests that could be run (NaN p-values are left out)."""
    tested = sorted((p, name) for name, p in pvalues.items() if p == p)
    out: Dict[str, Dict[str, Any]] = {name: {"p": p, "adjusted_p": None, "reject": None}
                                      for name, p in pvalues.items()}
    running, still_rejecting = 0.0, True
    for rank, (p, name) in enumerate(tested):
        running = max(running, min(1.0, (len(tested) - rank) * p))
        still_rejecting = still_rejecting and p <= alpha / (len(tested) - rank)
        out[name].update(adjusted_p=running, reject=still_rejecting)
    return out


def analyse(run_dirs: Sequence[Path], cfg: Dict[str, Any]) -> Dict[str, Any]:
    acfg = cfg["analysis"]
    runs = load_runs(run_dirs)
    rng = np.random.default_rng(int(cfg["seed"]))
    arms = list(runs[0]["y_pred"])
    for r in runs:
        if list(r["y_pred"]) != arms:
            raise ValueError(f"{r['run']} has detectors {list(r['y_pred'])}, not {arms}")
        if r["config"] != runs[0]["config"]:
            raise ValueError(f"{r['run']} was scored with a different config from {runs[0]['run']}")
    y = np.concatenate([r["y_true"] for r in runs])
    pred = {a: np.concatenate([r["y_pred"][a] for r in runs]) for a in arms}
    hits = {a: np.concatenate([r["segment_hits"][a] for r in runs]) for a in arms}
    n_segments = int(len(hits[arms[0]])) if arms else 0
    cats = np.concatenate([r["categories"] for r in runs])
    control = np.concatenate([r["control"] for r in runs])
    pooled = {a: {k: v for k, v in precision_recall_f1(y, pred[a]).items()} for a in arms}
    per_run = {r["run"]: {a: precision_recall_f1(r["y_true"], r["y_pred"][a]) for a in arms} for r in runs}

    samples = int(acfg["bootstrap_samples"])
    margin = float(acfg["viable_forfeiture_f1"])
    cold = np.concatenate([r["cold_start"] for r in runs])
    strengths = np.concatenate([r["strengths"] for r in runs])
    primary = [a for a in arms if a in PRIMARY_ARMS]
    h6 = None
    if "transfer" in pred and "transfer_similar" in pred:
        h6 = {**bootstrap_f1_gap(runs, "transfer_similar", "transfer", samples, rng),
              **mcnemar(y, pred["transfer_similar"], pred["transfer"])}
    families: Dict[str, Dict[str, Any]] = {}
    for source_free in SOURCE_FREE_ARMS:
        if source_free not in pred:
            continue
        tests: Dict[str, Any] = {}
        for name, baseline in HYPOTHESIS_BASELINES:
            if baseline in pred:
                ones = np.ones(n_segments, dtype=int)
                tests[name] = {"baseline": baseline, **bootstrap_f1_gap(runs, baseline, source_free, samples, rng),
                               **mcnemar(y, pred[baseline], pred[source_free]),
                               "segment_mcnemar": {
                                   "n_segments": n_segments,
                                   "n_detected": {baseline: int(hits[baseline].sum()),
                                                  source_free: int(hits[source_free].sum())},
                                   **mcnemar(ones, hits[baseline].astype(int), hits[source_free].astype(int)),
                               }}
        tests["H4"] = category_recall_test(y, pred[source_free], cats)
        tests["H5"] = {"detectors": primary, "false_alarm_rate": {a: float(pred[a][control].mean()) if control.any()
                                                                  else float("nan") for a in primary},
                       **cochran_q(np.column_stack([pred[a][control] for a in primary]))}
        if h6 is not None:
            tests["H6"] = dict(h6)
        decisions = {}
        for name, _ in HYPOTHESIS_BASELINES:
            if name in tests:
                upper, f1, thr = tests[name]["upper_one_sided_95"], pooled[source_free]["f1"], pooled["threshold"]["f1"]
                defined = not any(math.isnan(v) for v in (upper, f1, thr))
                non_inferior = bool(upper < margin) if defined else None
                decisions[tests[name]["baseline"]] = {
                    "non_inferior": non_inferior,
                    "above_threshold_alarms": bool(f1 > thr) if defined else None,
                    "viable_substitute": bool(non_inferior and f1 > thr) if defined else None}
        families[source_free] = {"tests": tests, "decisions": decisions}

    # One Holm family per application: H1 to H4 for each source-free detector, H5 and H6 once.
    pvalues = {}
    for fam, f in families.items():
        for h in ("H1", "H2", "H3", "H4"):
            if h in f["tests"]:
                pvalues[f"{h}:{fam}"] = f["tests"][h]["p"]
    for h in ("H5", "H6"):
        shared = [f["tests"][h]["p"] for f in families.values() if h in f["tests"]]
        if shared:
            pvalues[h] = shared[0]
    adjusted = holm(pvalues, float(acfg["alpha"]))
    for fam, f in families.items():
        f["tests"]["holm"] = {h: adjusted[f"{h}:{fam}" if f"{h}:{fam}" in adjusted else h]
                              for h in ("H1", "H2", "H3", "H4", "H5", "H6") if h in f["tests"]}

    # Supplementary, outside the Holm family.
    supplementary: Dict[str, Any] = {}
    if {"source_free", "source_free_forest", "novelty_gate"} <= set(pred):
        alarms = pred["source_free"] == 1
        supplementary["novelty_gate"] = {
            "f1": {a: pooled[a]["f1"] for a in ("source_free", "source_free_forest", "novelty_gate")},
            "alarms": int(alarms.sum()),
            "alarms_from_the_gate_only": int(np.sum(alarms & (pred["novelty_gate"] == 1) & (pred["source_free_forest"] == 0))),
            "alarms_from_the_forest_only": int(np.sum(alarms & (pred["novelty_gate"] == 0) & (pred["source_free_forest"] == 1))),
            "alarms_from_both": int(np.sum(alarms & (pred["novelty_gate"] == 1) & (pred["source_free_forest"] == 1)))}
    if {"transfer", "source_free_source_features"} <= set(pred):
        supplementary["feature_space"] = {
            "baseline": "transfer", "detector": "source_free_source_features",
            **bootstrap_f1_gap(runs, "transfer", "source_free_source_features", samples, rng)}
    supplementary["elasticity_false_alarms"] = {
        part: {"windows": int(mask.sum()),
               "false_alarm_rate": {a: float(pred[a][mask].mean()) if mask.any() else float("nan") for a in arms}}
        for part, mask in (("with_new_environment", control & cold), ("without_new_environment", control & ~cold))}
    supplementary["latency_recall_by_delay"] = {
        str(ms): {"windows": int(((strengths == ms) & (y == 1)).sum()),
                  "recall": {a: float(pred[a][(strengths == ms) & (y == 1)].mean()) for a in arms}}
        for ms in sorted(set(strengths[strengths > 0].tolist()))}
    return {"runs": [r["run"] for r in runs], "config": runs[0]["config"],
            "windows": int(len(y)), "positive_windows": int(y.sum()),
            "elasticity_windows": int(control.sum()), "pooled": pooled, "per_run": per_run,
            "detection_delay": {a: delay_summary([d for r in runs for d in r["segment_delays"][a]]) for a in arms},
            "families": families, "holm": adjusted, "supplementary": supplementary, "settings": dict(acfg)}


def _p(x: Optional[float]) -> str:
    return "n/a" if x is None or x != x else (f"{x:.2e}" if x < 1e-3 else f"{x:.3f}")


def render(result: Dict[str, Any]) -> str:
    lines = [f"# Analysis of the pooled runs: {', '.join(result['runs'])}", "",
             f"{result['windows']} windows pooled ({result['positive_windows']} positive, "
             f"{result['elasticity_windows']} fault-free elasticity windows).", "",
             "| Detector | Precision | Recall | F1 | MCC |", "|---|---:|---:|---:|---:|"]
    for arm, m in result["pooled"].items():
        lines.append(f"| {arm} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} | {m['mcc']:.4f} |")
    lines += ["", "Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.",
              "", "| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |",
              "|---|---:|---:|---:|---:|"]
    num = lambda x, f: "n/a" if x is None else format(x, f)
    for arm, d in result["detection_delay"].items():
        lines.append(f"| {arm} | {d['n_detected_segments']} of {d['n_segments']} | {num(d['mean_delay_windows'], '.2f')} | "
                     f"{num(d['median_delay_seconds'], '.1f')} | {num(d['mean_delay_seconds'], '.1f')} |")
    for source_free, fam in result["families"].items():
        t = fam["tests"]
        lines += ["", f"## Against {source_free}", "",
                  "| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |", "|---|---:|---|---:|---:|---|"]
        for h in ("H1", "H2", "H3", "H6"):
            if h in t:
                hol = t["holm"][h]
                lines.append(f"| {h} | {t[h]['gap']:+.4f} | [{t[h]['ci_low']:+.4f}, {t[h]['ci_high']:+.4f}] | "
                             f"{_p(t[h]['p'])} | {_p(hol['adjusted_p'])} | {hol['reject']} |")
        for h in ("H1", "H2", "H3"):
            if h in t and "segment_mcnemar" in t[h]:
                sm = t[h]["segment_mcnemar"]
                nd = sm["n_detected"]
                lines.append(f"| {h} (fault segments) | detected {'/'.join(f'{k} {v}' for k, v in nd.items())} "
                             f"of {sm['n_segments']} | | {_p(sm['p'])} | *(supplementary, not Holm-adjusted)* | |")
        for h, effect in (("H4", "recall " + ", ".join(f"{c} {r:.3f}" for c, r in t["H4"]["recall"].items())),
                          ("H5", "FAR " + ", ".join(f"{a} {v:.4f}" for a, v in t["H5"]["false_alarm_rate"].items()))):
            hol = t["holm"][h]
            lines.append(f"| {h} | {effect} | | {_p(t[h]['p'])} | {_p(hol['adjusted_p'])} | {hol['reject']} |")
        lines += ["", f"Non-inferiority (upper one-sided 95% bound of the forfeiture below {result['settings']['viable_forfeiture_f1']}) "
                  "and viability (also above the threshold alarms' F1):", "",
                  "| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |",
                  "|---|---:|---|---|---|"]
        for h, baseline in HYPOTHESIS_BASELINES:
            if baseline in fam["decisions"]:
                d = fam["decisions"][baseline]
                lines.append(f"| {baseline} | {t[h]['upper_one_sided_95']:+.4f} | {d['non_inferior']} | "
                             f"{d['above_threshold_alarms']} | {d['viable_substitute']} |")
    sup = result["supplementary"]
    lines += ["", "## Supplementary (not Holm-adjusted)", ""]
    if "novelty_gate" in sup:
        g = sup["novelty_gate"]
        lines.append(f"- Novelty gate: F1 {', '.join(f'{a} {v:.4f}' for a, v in g['f1'].items())}; of "
                     f"{g['alarms']} alarms of the combined detector, {g['alarms_from_the_gate_only']} come from the "
                     f"gate only, {g['alarms_from_the_forest_only']} from the forest only, {g['alarms_from_both']} from both.")
    if "feature_space" in sup:
        f = sup["feature_space"]
        lines.append(f"- Feature space: BGL-trained baseline minus the source-free detector on its features "
                     f"{f['gap']:+.4f} [{f['ci_low']:+.4f}, {f['ci_high']:+.4f}].")
    for part, v in sup["elasticity_false_alarms"].items():
        lines.append(f"- Elasticity windows {part.replace('_', ' ')} ({v['windows']}): false-alarm rate "
                     + ", ".join(f"{a} {_p(x) if x != x else format(x, '.4f')}" for a, x in v["false_alarm_rate"].items()))
    for ms, v in sup["latency_recall_by_delay"].items():
        lines.append(f"- Latency fault, {ms} ms delay ({v['windows']} fault windows): recall "
                     + ", ".join(f"{a} {x:.3f}" for a, x in v["recall"].items()))
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 2:
        print("usage: python -m sflad.pipeline.analysis OUT_DIR RUN_DIR [RUN_DIR ...]", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parents[3]
    cfg = load_config(root / "configs" / "default.yaml")
    out = Path(args[0])
    result = analyse([Path(p) for p in args[1:]], cfg)
    out.mkdir(parents=True, exist_ok=True)
    (out / "analysis.json").write_text(json.dumps(result, indent=2, default=float))
    (out / "analysis.md").write_text(render(result))
    print((out / "analysis.md").read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
