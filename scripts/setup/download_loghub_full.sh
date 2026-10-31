#!/usr/bin/env bash
# Download full LogHub corpora (Zenodo 10.5281/zenodo.8196385), verify MD5, extract.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DEST="$ROOT/data/public_corpus/full"
mkdir -p "$DEST"
cd "$DEST"

md5_of() { python3 -c "import hashlib,sys
h=hashlib.md5()
with open(sys.argv[1],'rb') as f:
    for chunk in iter(lambda: f.read(1<<20), b''): h.update(chunk)
print(h.hexdigest())" "$1"; }

fetch() {  # name expected_md5
  local name="$1" expected="$2"
  if [[ ! -f "$name" ]]; then
    curl -fL --retry 3 -o "$name" "https://zenodo.org/api/records/8196385/files/$name/content"
  fi
  local got; got="$(md5_of "$name")"
  if [[ "$got" != "$expected" ]]; then
    echo "MD5 mismatch for $name: got $got expected $expected" >&2
    exit 3
  fi
  echo "OK $name $got"
}

fetch BGL.zip 4452953c470f2d95fcb32d5f6e733f7a
fetch HDFS_v1.zip 76a24b4d9a6164d543fb275f89773260
fetch OpenStack.tar.gz 66bd42c07837a094d9b0ea2d036b5713

unzip -o -q BGL.zip BGL.log
unzip -o -q HDFS_v1.zip HDFS.log preprocessed/anomaly_label.csv
tar -xzf OpenStack.tar.gz
ls -la BGL.log HDFS.log preprocessed/anomaly_label.csv openstack_*.log anomaly_labels.txt
