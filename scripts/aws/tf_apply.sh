#!/usr/bin/env bash
# Init and apply the Terraform evaluation stack in AWS.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TF_DIR="$ROOT/infra/terraform"

# Use the default AWS endpoints.
unset AWS_ENDPOINT_URL
REGION="$(sed -n 's/^region: *\([^ #]*\).*/\1/p' "$ROOT/configs/aws.yaml" | tr -d "\r\"'")"
[[ -n "$REGION" ]] || { echo "configs/aws.yaml has no region line" >&2; exit 1; }
export AWS_DEFAULT_REGION="$REGION" AWS_REGION="$REGION"

cd "$TF_DIR"
terraform init -input=false  # .terraform.lock.hcl pins the providers
terraform apply -auto-approve -var "aws_region=$REGION" "$@"
echo "--- outputs ---"
terraform output -json
