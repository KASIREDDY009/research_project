from __future__ import annotations

from synthetic_data import synthetic_config

from pathlib import Path

from sflad.data.loghub import load_bgl, load_hdfs, load_openstack, split_chronological

ROOT = Path(__file__).resolve().parents[1]

BGL = (
    "- 1117838570 2005.06.03 R02-M1-N0-C:J12-U11 2005-06-03-15.42.50.363779 "
    "R02-M1-N0-C:J12-U11 RAS KERNEL INFO instruction cache parity error corrected\n"
    "KERNDTLB 1118536327 2005.06.11 R30-M0-N9-C:J16-U01 2005-06-11-17.32.07.581048 "
    "R30-M0-N9-C:J16-U01 RAS KERNEL FATAL data TLB error interrupt\n"
)
HDFS_LOG = (
    "081109 203518 143 INFO dfs.DataNode$DataXceiver: Receiving block blk_-1608999687919862906 "
    "src: /10.250.19.102:54106 dest: /10.250.19.102:50010\n"
    "081109 203519 145 WARN dfs.DataNode$DataXceiver: writeBlock blk_7503483334202473044 "
    "received exception java.io.IOException\n"
)
HDFS_LABELS = "BlockId,Label\nblk_-1608999687919862906,Normal\nblk_7503483334202473044,Anomaly\n"
OS_LABELS = (
    "The following VM instances have injected anomalies as observed in openstack_abnormal.log.\n\n"
    "544fd51c-4edc-4780-baae-ba1d80a0acfc\n"
)
OS_ABNORMAL = (
    "nova-compute.log.2017-05-14_21:27:09 2017-05-14 19:39:02.007 2931 INFO nova.compute.manager "
    "[req-3ea4052c-895d-4b64-9e2d-04d64c4d94ab - - - - -] "
    "[instance: 544fd51c-4edc-4780-baae-ba1d80a0acfc] VM Started (Lifecycle Event)\n"
)
OS_NORMAL = (
    "nova-api.log.2017-05-14_21:27:04 2017-05-14 19:39:01.445 25746 INFO nova.osapi_compute.wsgi.server "
    "[req-5a2050e7-b381-4ae9-92d2-8b08e9f9f4c0 113d3a99c3da401fbd62cc2caa5b96d2 "
    '54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/servers/detail HTTP/1.1" status: 200\n'
)


def test_load_bgl_labels_and_levels(tmp_path):
    p = tmp_path / "BGL.log"
    p.write_text(BGL)
    ev = load_bgl(p)
    assert [e.is_anomaly for e in ev] == [False, True]
    assert [e.level for e in ev] == ["INFO", "ERROR"]  # from the log's own severity, not the label
    assert [e.message for e in ev] == ["instruction cache parity error corrected", "data TLB error interrupt"]
    assert ev[0].split == "source"
    assert [e.meta["loghub_label"] for e in ev] == ["-", "KERNDTLB"]


def test_load_bgl_respects_max_lines(tmp_path):
    p = tmp_path / "BGL.log"
    p.write_text(BGL)
    assert len(load_bgl(p, max_lines=1)) == 1


def test_load_hdfs_block_labels(tmp_path):
    (tmp_path / "HDFS.log").write_text(HDFS_LOG)
    (tmp_path / "anomaly_label.csv").write_text(HDFS_LABELS)
    ev = load_hdfs(tmp_path / "HDFS.log", tmp_path / "anomaly_label.csv")
    assert [e.is_anomaly for e in ev] == [False, True]
    assert [e.level for e in ev] == ["INFO", "WARNING"]
    assert ev[1].message == "writeBlock blk_7503483334202473044 received exception java.io.IOException"


def test_load_hdfs_groups_lines_by_block(tmp_path):
    lines = [
        "081109 203518 143 INFO dfs.DataNode$DataXceiver: Receiving block blk_1",
        "081109 203518 144 INFO dfs.DataNode$DataXceiver: Receiving block blk_2",
        "081109 203519 145 INFO dfs.DataNode$PacketResponder: PacketResponder 0 for block blk_1 terminating",
        "081109 203519 146 WARN dfs.DataNode$DataXceiver: writeBlock blk_2 received exception java.io.IOException",
    ]
    (tmp_path / "HDFS.log").write_text("\n".join(lines) + "\n")
    (tmp_path / "anomaly_label.csv").write_text("BlockId,Label\nblk_1,Normal\nblk_2,Anomaly\n")
    ev = load_hdfs(tmp_path / "HDFS.log", tmp_path / "anomaly_label.csv", group_by_block=True)
    assert [e.message.split()[-1] for e in ev] == ["blk_1", "terminating", "blk_2", "java.io.IOException"]
    assert [e.is_anomaly for e in ev] == [False, False, True, True]
    assert [e.timestamp_ms for e in ev] == [0, 1, 2, 3]


def test_load_openstack_instance_labels(tmp_path):
    (tmp_path / "anomaly_labels.txt").write_text(OS_LABELS)
    (tmp_path / "openstack_normal1.log").write_text(OS_NORMAL)
    (tmp_path / "openstack_abnormal.log").write_text(OS_ABNORMAL)
    ev = load_openstack(
        [tmp_path / "openstack_normal1.log", tmp_path / "openstack_abnormal.log"],
        tmp_path / "anomaly_labels.txt",
    )
    assert [e.is_anomaly for e in ev] == [False, True]
    assert {e.level for e in ev} == {"INFO"}
    assert ev[1].message == "[instance: 544fd51c-4edc-4780-baae-ba1d80a0acfc] VM Started (Lifecycle Event)"


def test_load_openstack_whole_file_labels(tmp_path):
    (tmp_path / "anomaly_labels.txt").write_text(OS_LABELS)
    (tmp_path / "openstack_normal1.log").write_text(OS_NORMAL)
    (tmp_path / "openstack_abnormal.log").write_text(OS_NORMAL + OS_ABNORMAL)
    ev = load_openstack(
        [tmp_path / "openstack_normal1.log", tmp_path / "openstack_abnormal.log"],
        tmp_path / "anomaly_labels.txt",
        anomalous_files=[tmp_path / "openstack_abnormal.log"],
    )
    assert [e.is_anomaly for e in ev] == [False, True, True]


def test_split_chronological_first_half_is_train(tmp_path):
    p = tmp_path / "BGL.log"
    p.write_text(BGL * 5)  # 10 lines
    ev = split_chronological(load_bgl(p), 0.5)
    assert [e.split for e in ev] == ["train"] * 5 + ["eval"] * 5


def test_build_source_writes_bgl_jsonl(tmp_path):
    from scripts.setup.build_source import main
    from sflad.data.event_io import events_from_jsonl

    src = tmp_path / "BGL.log"
    src.write_text(BGL)
    out = tmp_path / "source.jsonl"
    assert main(["BGL", "--input", str(src), "--out", str(out)]) == 0
    ev = events_from_jsonl(out)
    assert [e.level for e in ev] == ["INFO", "ERROR"] and all(e.split == "source" for e in ev)


def test_default_baseline_transfers_from_the_bgl_2k_sample(tmp_path):
    from synthetic_logs import generate_dataset
    from sflad.detectors.transfer import TransferDetector
    from sflad.pipeline.metrics import false_alarm_rate, precision_recall_f1
    from sflad.pipeline.train_eval import events_from_jsonl

    cfg = synthetic_config()
    generate_dataset(cfg, tmp_path)
    target = events_from_jsonl(tmp_path / "events.jsonl")
    source = load_bgl(ROOT / "data" / "public_corpus" / "BGL" / "BGL_2k.log")
    det = TransferDetector(window_size=20, step_size=20, random_state=42)
    res = det.fit(target, source_events=source).predict(target)
    assert precision_recall_f1(res.y_true, res.y_pred)["mcc"] > 0.5
    assert false_alarm_rate(res.y_true, res.y_pred) <= 0.1


def test_openstack_critical_is_an_error_level(tmp_path):
    line = (
        "nova-api.log.2017-05-14_21:27:04 2017-05-14 19:39:01.445 25746 CRITICAL "
        "keystonemiddleware.auth_token [-] Unable to validate token\n"
    )
    (tmp_path / "anomaly_labels.txt").write_text(OS_LABELS)
    (tmp_path / "openstack_normal1.log").write_text(line)
    ev = load_openstack([tmp_path / "openstack_normal1.log"], tmp_path / "anomaly_labels.txt")
    assert ev[0].level == "ERROR"


def test_bgl_line_with_a_missing_header_field_keeps_its_severity(tmp_path):
    line = "- 1119415930 2005.06.21 - 2005-06-21-21.52.10.214285 RAS KERNEL FATAL Kill job 20251 timed out. Block freed.\n"
    (tmp_path / "BGL.log").write_text(BGL + line)
    ev = load_bgl(tmp_path / "BGL.log")
    assert ev[2].level == "ERROR"
    assert ev[2].message == "Kill job 20251 timed out. Block freed."
    assert [e.level for e in ev[:2]] == ["INFO", "ERROR"]


def test_a_line_without_a_severity_token_is_unknown(tmp_path):
    trace = '  File "/usr/lib/python2.7/dist-packages/nova/compute/manager.py", line 123, in _build\n'
    (tmp_path / "anomaly_labels.txt").write_text(OS_LABELS)
    (tmp_path / "openstack_normal1.log").write_text(OS_NORMAL + trace)
    ev = load_openstack([tmp_path / "openstack_normal1.log"], tmp_path / "anomaly_labels.txt")
    assert [e.level for e in ev] == ["INFO", "UNKNOWN"]
