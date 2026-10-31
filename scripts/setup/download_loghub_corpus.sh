#!/usr/bin/env bash
# Download the LogHub BGL_2k sample, check it against its pin in configs/corpus.yaml, build the
# BGL-trained baseline's source_events.jsonl, check it too and write SHA256SUMS.txt. The OpenStack
# source ships in the repository; scripts/setup/build_source.py OpenStack rebuilds it from the full
# LogHub OpenStack set (scripts/setup/download_loghub_full.sh).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CORPUS="$ROOT/data/public_corpus"
mkdir -p "$CORPUS/BGL"
cd "$CORPUS"

BGL_URL="https://raw.githubusercontent.com/logpai/loghub/master/BGL/BGL_2k.log"
EXPECTED_BGL="$(python3 -c 'import sys, yaml; print(yaml.safe_load(open(sys.argv[1]))["baseline_source"]["sha256"]["BGL_2k.log"])' "$ROOT/configs/corpus.yaml")"

echo "Fetching $BGL_URL -> BGL/BGL_2k.log"
if ! curl -fsSL --max-time 120 -o BGL/BGL_2k.log "$BGL_URL"; then
  echo "DOWNLOAD FAILED for $BGL_URL" >&2
  exit 2
fi

got_bgl="$(sha256sum BGL/BGL_2k.log | awk '{print $1}')"
if [[ "$got_bgl" != "$EXPECTED_BGL" ]]; then
  echo "BGL/BGL_2k.log has sha256 $got_bgl, not the pinned one" >&2
  exit 3
fi

python3 "$ROOT/scripts/setup/build_source.py" BGL --input BGL/BGL_2k.log --out BGL/source_events.jsonl

EXPECTED_SRC="$(python3 -c 'import sys, yaml; print(yaml.safe_load(open(sys.argv[1]))["baseline_source"]["sha256"]["source_events.jsonl"])' "$ROOT/configs/corpus.yaml")"
got_src="$(sha256sum BGL/source_events.jsonl | awk '{print $1}')"
if [[ "$got_src" != "$EXPECTED_SRC" ]]; then
  echo "BGL/source_events.jsonl has sha256 $got_src, not the pinned one" >&2
  exit 3
fi
sha256sum BGL/BGL_2k.log BGL/source_events.jsonl OpenStack/source_events.jsonl | tee SHA256SUMS.txt
