#!/usr/bin/env bash
# Scores two exported evaluation runs of different applications as SageMaker jobs: every detector on each,
# with the other's labelled events as the similar-application baseline's source.
# Usage: ./scripts/aws/score_pair.sh RUN_A RUN_B
#   RUN_A, RUN_B: results/runs/<tag>/<app> folders, one orders and one bookings, from the same set of runs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
if [[ -f .venv/bin/activate ]]; then
  source .venv/bin/activate
fi
RUN_A="${1:?usage: score_pair.sh RUN_A RUN_B}"
RUN_B="${2:?usage: score_pair.sh RUN_A RUN_B}"
unset AWS_ENDPOINT_URL
export PYTHONUNBUFFERED=1

for run in "$RUN_A" "$RUN_B"; do
  [[ -f "$run/raw/events.jsonl" ]] || { echo "$run/raw/events.jsonl missing; run run_evaluation.sh first." >&2; exit 1; }
done
APP_A="$(basename "$RUN_A")"
APP_B="$(basename "$RUN_B")"
[[ "$APP_A" != "$APP_B" ]] || { echo "RUN_A and RUN_B are both '$APP_A'; pass one of each application." >&2; exit 1; }
if ! aws sts get-caller-identity >/dev/null; then
  echo "The AWS CLI has no working credentials; sign in before scoring." >&2
  exit 1
fi
TAG="$(basename "$(dirname "$RUN_A")")-$(basename "$(dirname "$RUN_B")")"

score() {
  local run="$1" app="$2" other_raw="$3"
  if [[ -e "$run/processed" ]]; then
    echo "$run/processed already exists; it is never overwritten." >&2
    return 1
  fi
  python scripts/aws/run_on_sagemaker.py --name "eval-$TAG-$app" \
    --input "raw-$TAG-$app=$run/raw" --input "other-$TAG-$app=$other_raw" \
    --output "$run/processed" \
    "mkdir -p /tmp/run && cp -r \"\$IN/raw-$TAG-$app\" /tmp/run/raw && python scripts/scoring/evaluate_run.py /tmp/run --similar-source \"\$IN/other-$TAG-$app/events.jsonl\" && cp -r /tmp/run/processed/. \"\$OUT/\"" \
    >"$run/evaluate.log" 2>&1
}

pids=()
score "$RUN_A" "$APP_A" "$RUN_B/raw" & pids+=($!)
score "$RUN_B" "$APP_B" "$RUN_A/raw" & pids+=($!)
failed=0
for pid in "${pids[@]}"; do
  wait "$pid" || failed=1
done
[[ $failed -eq 0 ]] || { echo "Scoring failed; see $RUN_A/evaluate.log and $RUN_B/evaluate.log" >&2; exit 1; }
echo "Scored: $RUN_A and $RUN_B"
