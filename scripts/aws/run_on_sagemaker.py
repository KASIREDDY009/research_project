#!/usr/bin/env python3
"""Run a command from this repository as a SageMaker processing job.

Uploads the code of this folder (without the virtual environments, results, the full LogHub
downloads or Terraform state) and every --input directory, runs COMMAND with $IN
and $OUT set, and downloads $OUT into --output. The launcher waits while every job slot is busy.

  python scripts/aws/run_on_sagemaker.py --name calib-openstack --input corpus=LOCAL_DIR \\
      --output results/calibration/parts/openstack \\
      'python scripts/scoring/calibrate_transfer_loghub.py --pairs OpenStack --openstack-dir "$IN/corpus" --out "$OUT"'
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

ROOT = Path(__file__).resolve().parents[2]
IMAGE = "763104351884.dkr.ecr.{region}.amazonaws.com/pytorch-training:2.6.0-cpu-py312-ubuntu22.04-sagemaker"
BASE = "/opt/ml/processing"
# Paths under ROOT that are not code: environments, outputs, downloads and Terraform state.
SKIP_DIRS = {".git", ".venv", "results", "__pycache__", ".pytest_cache", ".terraform",
             "data/public_corpus/full", "infra/terraform/build"}
SKIP_FILE = re.compile(r"(\.pyc|\.tfstate(\..*)?|\.tfplan|^terraform\.tfvars|^\.DS_Store|^sflad-evaluation-runs\.tar\.gz(\.sha256)?)$")


def job_script(command: str) -> str:
    """Unpack the code, install its requirements, then run the command with $IN and $OUT set."""
    return "\n".join([
        "set -euo pipefail",
        "mkdir -p /opt/code",
        f"tar -xzf {BASE}/input/code/code.tar.gz -C /opt/code",
        "cd /opt/code",
        "pip install --quiet --no-cache-dir -r requirements.txt",
        f"export IN={BASE}/input OUT={BASE}/output PYTHONUNBUFFERED=1",
        command,
        "",
    ])


def upload_tree(s3, bucket: str, prefix: str, local: Path) -> None:
    """Upload every file under local to s3://bucket/prefix/ (a prefix used by one job only)."""
    for path in sorted(p for p in local.rglob("*") if p.is_file()):
        s3.upload_file(str(path), bucket, f"{prefix}/{path.relative_to(local).as_posix()}")


def download_tree(s3, bucket: str, prefix: str, local: Path) -> None:
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix + "/"):
        for obj in page.get("Contents", []):
            dest = local / obj["Key"][len(prefix) + 1:]
            dest.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(bucket, obj["Key"], str(dest))


def pack_code(dest: Path) -> None:
    """Write the code of ROOT to dest as a .tar.gz, leaving out SKIP_DIRS and SKIP_FILE."""
    def keep(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
        rel = info.name.removeprefix("./")
        parts = rel.split("/")
        if any("/".join(parts[:i + 1]) in SKIP_DIRS or parts[i] in SKIP_DIRS or parts[i].endswith(".egg-info")
               for i in range(len(parts))):
            return None
        return None if info.isfile() and SKIP_FILE.search(parts[-1]) else info
    with tarfile.open(dest, "w:gz") as tar:
        tar.add(ROOT, arcname=".", filter=keep)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", required=True, help="letters, digits and hyphens")
    p.add_argument("--input", action="append", default=[], metavar="NAME=DIR")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--instance", default="ml.t3.xlarge")
    p.add_argument("--volume-gb", type=int, default=40)
    p.add_argument("--max-hours", type=float, default=12.0)
    p.add_argument("command")
    a = p.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9-]+", a.name):
        raise SystemExit("--name takes lower-case letters, digits and hyphens")

    tf = subprocess.run(["terraform", f"-chdir={ROOT / 'infra' / 'terraform'}", "output", "-json", "compute"],
                        capture_output=True, text=True, check=True)
    compute = json.loads(tf.stdout)
    bucket, region = compute["bucket"], compute["region"]
    job = f"sflad-{a.name}-{time.strftime('%m%d-%H%M%S')}"
    s3 = boto3.client("s3", region_name=region)
    with tempfile.TemporaryDirectory() as tmp:
        code = Path(tmp)
        pack_code(code / "code.tar.gz")
        (code / "job.sh").write_text(job_script(a.command))
        upload_tree(s3, bucket, f"jobs/{job}/code", code)
    inputs = [{"InputName": "code", "S3Input": {"S3Uri": f"s3://{bucket}/jobs/{job}/code", "LocalPath": f"{BASE}/input/code",
                                                 "S3DataType": "S3Prefix", "S3InputMode": "File"}}]
    for spec in a.input:
        name, local = spec.split("=", 1)
        if not re.fullmatch(r"[a-z0-9-]+", name):
            raise SystemExit(f"input name {name!r} takes lower-case letters, digits and hyphens")
        upload_tree(s3, bucket, f"jobs/{job}/inputs/{name}", Path(local))
        inputs.append({"InputName": name, "S3Input": {"S3Uri": f"s3://{bucket}/jobs/{job}/inputs/{name}",
                                                      "LocalPath": f"{BASE}/input/{name}",
                                                      "S3DataType": "S3Prefix", "S3InputMode": "File"}})

    sm = boto3.client("sagemaker", region_name=region)
    request = dict(
        ProcessingJobName=job,
        ProcessingResources={"ClusterConfig": {"InstanceCount": 1, "InstanceType": a.instance,
                                               "VolumeSizeInGB": a.volume_gb}},
        StoppingCondition={"MaxRuntimeInSeconds": int(a.max_hours * 3600)},
        AppSpecification={"ImageUri": IMAGE.format(region=region),
                          "ContainerEntrypoint": ["bash", f"{BASE}/input/code/job.sh"]},
        ProcessingInputs=inputs,
        ProcessingOutputConfig={"Outputs": [{"OutputName": "out", "S3Output": {
            "S3Uri": f"s3://{bucket}/jobs/{job}/output", "LocalPath": f"{BASE}/output", "S3UploadMode": "EndOfJob"}}]},
        RoleArn=compute["role_arn"],
    )
    while True:
        try:
            sm.create_processing_job(**request)
            break
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceLimitExceeded":
                raise
            print(f"{job}: no job slot is free (all busy, or the region's quota '{a.instance} for processing job usage' is too low); "
                  "retrying in 5 min", flush=True)
            time.sleep(300)
    print(f"{job}: started on {a.instance}", flush=True)

    status, started = None, time.time()
    while status not in ("Completed", "Failed", "Stopped"):
        time.sleep(60)
        desc = sm.describe_processing_job(ProcessingJobName=job)
        if desc["ProcessingJobStatus"] != status:
            status = desc["ProcessingJobStatus"]
            print(f"{job}: {status} after {(time.time() - started) / 60:.0f} min", flush=True)
    if status != "Completed":
        print(f"{job}: {desc.get('FailureReason', '')}", file=sys.stderr)
        logs = boto3.client("logs", region_name=region)
        try:
            events = logs.filter_log_events(logGroupName="/aws/sagemaker/ProcessingJobs",
                                            logStreamNamePrefix=job)["events"]
            for e in events[-40:]:
                print(e["message"].rstrip(), file=sys.stderr)
        except ClientError:
            pass
        return 1
    a.output.mkdir(parents=True, exist_ok=True)
    download_tree(s3, bucket, f"jobs/{job}/output", a.output)
    print(f"{job}: outputs in {a.output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
