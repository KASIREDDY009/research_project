#!/usr/bin/env bash
# Destroy the Terraform evaluation stack.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TF_DIR="$ROOT/infra/terraform"

unset AWS_ENDPOINT_URL
REGION="$(sed -n 's/^region: *\([^ #]*\).*/\1/p' "$ROOT/configs/aws.yaml" | tr -d "\r\"'")"
[[ -n "$REGION" ]] || { echo "configs/aws.yaml has no region line" >&2; exit 1; }
export AWS_DEFAULT_REGION="$REGION" AWS_REGION="$REGION"

cd "$TF_DIR"
terraform init -input=false
terraform destroy -auto-approve -var "aws_region=$REGION" "$@"
