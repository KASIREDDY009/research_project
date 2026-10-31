#!/usr/bin/env bash
# One evaluation run on both applications in parallel: requests, faults, elasticity bursts and the labelled
# log export. Usage: ./scripts/aws/run_evaluation.sh TAG SEED   (TAG: lower-case letters, digits, hyphens; outputs
# under results/runs/TAG/<app>/raw). Needs the deployed stack (./scripts/aws/tf_apply.sh); scripts/aws/score_pair.sh scores it.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
if [[ -f .venv/bin/activate ]]; then
  source .venv/bin/activate
fi
TAG="${1:?usage: run_evaluation.sh TAG SEED}"
SEED="${2:?usage: run_evaluation.sh TAG SEED}"
OUT="results/runs/$TAG"
unset AWS_ENDPOINT_URL
export PYTHONUNBUFFERED=1

if [[ ! "$TAG" =~ ^[a-z0-9-]+$ ]]; then
  echo "TAG takes lower-case letters, digits and hyphens (got '$TAG')." >&2
  exit 1
fi
if [[ -e "$OUT" ]]; then
  echo "$OUT already exists; choose a new tag (an existing run folder is never overwritten)." >&2
  exit 1
fi
if ! aws sts get-caller-identity >/dev/null; then
  echo "The AWS CLI has no working credentials; sign in before the evaluation run." >&2
  exit 1
fi
mkdir -p "$OUT"

pids=()
# An interrupt reaches both applications' processes, which restore the deployed settings before they stop.
trap 'kill -TERM ${pids[@]+"${pids[@]}"} 2>/dev/null; wait; exit 130' INT TERM HUP
for app in orders bookings; do
  mkdir -p "$OUT/$app"
  python -m sflad.aws.evaluation_run --app "$app" --out "$OUT/$app" --seed "$SEED" >"$OUT/$app/run.log" 2>&1 &
  pids+=($!)
done
failed=0
for i in 0 1; do
  if ! wait "${pids[$i]}"; then
    failed=1
  fi
done
[[ $failed -eq 0 ]] || { echo "Evaluation run $TAG finished with a failure; see $OUT/*/run.log" >&2; exit 1; }
echo "Evaluation run $TAG complete: $OUT"
