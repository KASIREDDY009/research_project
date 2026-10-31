"""Parser masking must stabilize CloudWatch-shaped templates."""

from __future__ import annotations

from sflad.data.schema import LogEvent
from sflad.detectors.source_free import SourceFreeDetector
from sflad.parsing.template_parser import TemplateParser, _mask_variables


def test_iso_timestamp_milliseconds_masked():
    a = (
        "[ERROR]\t2026-09-19T07:22:17.806Z\tc2242128-c21e-426f-8895-60fea68a42e5\t"
        '{"event": "AccessDeniedException", "message": "denied"}'
    )
    b = (
        "[ERROR]\t2026-09-19T07:22:18.091Z\td3353239-d32f-5370-99a6-71afb79b53f6\t"
        '{"event": "AccessDeniedException", "message": "denied"}'
    )
    ma, mb = _mask_variables(a), _mask_variables(b)
    assert "<TS>" in ma
    assert ".806Z" not in ma
    assert ma == mb


def test_letter_prefixed_id_with_no_separator_is_masked():
    """A zero-padded id fused onto a letter prefix ("V133318") collapses across distinct ids."""
    a = "booking b: 3 guests at V133318 (city-40) slot 4"
    b = "booking b: 1 guests at V000042 (city-90) slot 9"
    ma, mb = _mask_variables(a), _mask_variables(b)
    assert ma == mb
    assert "V133318" not in ma
    assert "V000042" not in mb


def test_parser_collapses_error_lines():
    parser = TemplateParser()
    msgs = [
        '[ERROR]\t2026-09-19T07:22:17.806Z\tc2242128-c21e-426f-8895-60fea68a42e5\t{"event": "AccessDeniedException"}',
        '[ERROR]\t2026-09-19T07:22:18.091Z\td3353239-d32f-5370-99a6-71afb79b53f6\t{"event": "AccessDeniedException"}',
        '[ERROR]\t2026-09-19T07:22:19.396Z\te4464340-e43a-6481-aab7-82afc80c64a7\t{"event": "AccessDeniedException"}',
    ]
    ids = [parser.parse(m).template_id for m in msgs]
    assert len(set(ids)) == 1


def test_source_free_fires_on_novel_error_after_clean_train():
    train = [
        LogEvent(
            timestamp_ms=i,
            message=f"INFO order created id={i:04d}",
            level="INFO",
            is_anomaly=False,
            split="train",
        )
        for i in range(80)
    ]
    eval_clean = [
        LogEvent(
            timestamp_ms=1000 + i,
            message=f"INFO order created id={i:04d}",
            level="INFO",
            is_anomaly=False,
            split="eval",
        )
        for i in range(40)
    ]
    eval_fault = [
        LogEvent(
            timestamp_ms=2000 + i,
            message=(
                f"[ERROR]\t2026-09-19T07:22:17.{100 + i:03d}Z\t"
                "c2242128-c21e-426f-8895-60fea68a42e5\t"
                '{"event": "AccessDeniedException", "message": '
                '"denied requestId=c2242128-c21e-426f-8895-60fea68a42e5"}'
            ),
            level="ERROR",
            is_anomaly=True,
            split="eval",
            fault_category="permission",
        )
        for i in range(20)
    ]
    events = train + eval_clean + eval_fault
    det = SourceFreeDetector(
        window_size=10,
        step_size=5,
        calib_fpr=0.1,
        random_state=0,
    )
    det.fit(events)
    res = det.predict(events)
    assert res.y_pred.sum() > 0, "the source-free detector must not predict all-normal when ERROR faults exist"
    tp = int(((res.y_pred == 1) & (res.y_true == 1)).sum())
    assert tp > 0


def test_parser_masks_timestamps_and_request_ids():
    """Two lines that differ only in timestamp and request id share one template."""
    from sflad.parsing.template_parser import build_parser, _mask_variables

    msg_a = '[ERROR]\t2026-09-19T07:22:17.806Z\tc2242128-c21e-426f-8895-60fea68a42e5\t{"event": "AccessDeniedException"}'
    msg_b = '[ERROR]\t2026-09-19T07:22:18.091Z\td3353239-d32f-5370-99a6-71afb79b53f6\t{"event": "AccessDeniedException"}'
    assert _mask_variables(msg_a) == _mask_variables(msg_b)
    parser = build_parser()
    assert parser.parse(msg_a).template_id == parser.parse(msg_b).template_id
