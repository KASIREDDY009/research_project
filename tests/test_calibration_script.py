from __future__ import annotations

import json
import math


def _bgl(n: int) -> str:
    lines = []
    for i in range(n):
        if i % 10 == 9:
            lines.append(f"KERNDTLB 1118536327 2005.06.11 R30 2005-06-11-17.32.07.{i:06d} R30 RAS KERNEL FATAL data TLB error interrupt")
        else:
            lines.append(f"- 1117838570 2005.06.03 R02 2005-06-03-15.42.50.{i:06d} R02 RAS KERNEL INFO generating core")
    return "\n".join(lines) + "\n"


def _hdfs(n: int) -> tuple[str, str]:
    lines, labels = [], ["BlockId,Label"]
    for i in range(n):
        blk = f"blk_{1000 + i}"
        bad = i % 10 == 9
        level = "WARN" if bad else "INFO"
        msg = "received exception java.io.IOException" if bad else "Receiving block"
        lines.append(f"081109 2035{i % 60:02d} 143 {level} dfs.DataNode$DataXceiver: {msg} {blk}")
        labels.append(f"{blk},{'Anomaly' if bad else 'Normal'}")
    return "\n".join(lines) + "\n", "\n".join(labels) + "\n"


def test_calibration_writes_f1_and_mcc_for_both_pairs(tmp_path):
    from scripts.scoring.calibrate_transfer_loghub import main

    (tmp_path / "BGL.log").write_text(_bgl(200))
    log, labels = _hdfs(200)
    (tmp_path / "HDFS.log").write_text(log)
    (tmp_path / "anomaly_label.csv").write_text(labels)
    uuid = "544fd51c-4edc-4780-baae-ba1d80a0acfc"
    (tmp_path / "anomaly_labels.txt").write_text(f"header line\n\n{uuid}\n")
    normal = "".join(
        f"nova-api.log 2017-05-14 19:39:01.{i:03d} 25746 INFO nova.osapi_compute.wsgi.server GET servers status: 200\n"
        for i in range(120)
    )
    abnormal = "".join(
        f"nova-compute.log 2017-05-14 19:39:02.{i:03d} 2931 INFO nova.compute.manager [instance: {uuid}] VM Started\n"
        for i in range(40)
    )
    (tmp_path / "openstack_normal1.log").write_text(normal)
    (tmp_path / "openstack_abnormal.log").write_text(abnormal)
    out = tmp_path / "calib"
    rc = main([
        "--bgl", str(tmp_path / "BGL.log"),
        "--hdfs-log", str(tmp_path / "HDFS.log"),
        "--hdfs-labels", str(tmp_path / "anomaly_label.csv"),
        "--openstack-dir", str(tmp_path),
        "--window", "5", "--step", "5", "--out", str(out),
    ])
    assert rc == 0
    data = json.loads((out / "calibration.json").read_text())
    for pair in ("BGL->HDFS", "BGL->OpenStack"):
        r = data["results"][pair]
        v = r["baseline"]
        assert 0.0 <= v["f1"] <= 1.0  # the scored half has anomalies, so F1 is defined
        assert math.isnan(v["mcc"]) or -1.0 <= v["mcc"] <= 1.0
        assert v["tp"] + v["fp"] + v["fn"] + v["tn"] == v["meta"]["n_windows"]
        assert r["elfa_log_reference"] == {"BGL->HDFS": {"f1": 71.83, "mcc": 0.674},
                                           "BGL->OpenStack": {"f1": 58.43, "mcc": 0.054}}[pair]
        assert r["n_target_anomalous_events"] > 0
        assert r["baseline"]["meta"]["calib_fpr"] == 0.01  # the configured baseline
    assert data["results"]["BGL->HDFS"]["n_target_events"] == 200
    assert data["results"]["BGL->OpenStack"]["n_target_events"] == 160
    assert data["corpora"]["OpenStack"] == {
        "events": 160, "anomalous_events": 40, "elfa_log": {"messages": 70_724, "anomalies": 18_435}
    }
    assert data["corpora"]["BGL"]["anomalous_events"] == 20
    assert set(data["settings"]["inputs"]) == {
        "BGL.log", "HDFS.log", "anomaly_label.csv", "openstack_normal1.log", "openstack_abnormal.log",
        "anomaly_labels.txt",
    }
    assert str(tmp_path) not in (out / "calibration.json").read_text()  # no machine paths recorded
    b = data["results"]["BGL->HDFS"]["baseline"]["per_block"]
    assert b["n_blocks"] > 0 and b["tp"] + b["fp"] + b["fn"] + b["tn"] == b["n_blocks"]
    assert (out / "calibration.md").read_text().startswith("# BGL-trained baseline on public LogHub transfer pairs")


def test_parts_merge_into_one_calibration(tmp_path):
    from scripts.scoring.calibrate_transfer_loghub import main

    (tmp_path / "BGL.log").write_text(_bgl(200))
    log, labels = _hdfs(200)
    (tmp_path / "HDFS.log").write_text(log)
    (tmp_path / "anomaly_label.csv").write_text(labels)
    uuid = "544fd51c-4edc-4780-baae-ba1d80a0acfc"
    (tmp_path / "anomaly_labels.txt").write_text(f"header line\n\n{uuid}\n")
    (tmp_path / "openstack_normal1.log").write_text("".join(
        f"nova-api.log 2017-05-14 19:39:01.{i:03d} 25746 INFO nova.osapi_compute.wsgi.server GET servers status: 200\n"
        for i in range(120)))
    (tmp_path / "openstack_abnormal.log").write_text("".join(
        f"nova-compute.log 2017-05-14 19:39:02.{i:03d} 2931 INFO nova.compute.manager [instance: {uuid}] VM Started\n"
        for i in range(40)))
    common = ["--bgl", str(tmp_path / "BGL.log"), "--hdfs-log", str(tmp_path / "HDFS.log"),
              "--hdfs-labels", str(tmp_path / "anomaly_label.csv"), "--openstack-dir", str(tmp_path),
              "--window", "5", "--step", "5"]
    assert main(common + ["--pairs", "HDFS", "--out", str(tmp_path / "a")]) == 0
    assert main(common + ["--pairs", "OpenStack", "--out", str(tmp_path / "b")]) == 0
    parts = [str(tmp_path / d / "calibration.json") for d in "ab"]
    assert main(["--merge", *parts, "--out", str(tmp_path / "all")]) == 0
    merged = json.loads((tmp_path / "all" / "calibration.json").read_text())
    assert list(merged["results"]) == ["BGL->HDFS", "BGL->OpenStack"]
    assert "baseline" in merged["results"]["BGL->HDFS"]
    assert set(merged["corpora"]) == {"BGL", "HDFS", "OpenStack"}
    assert "HDFS scored per block session" in (tmp_path / "all" / "calibration.md").read_text()
