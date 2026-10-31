# Training runs as SageMaker processing jobs: inputs and outputs pass through this bucket.
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "compute" {
  bucket        = "sflad-compute-${data.aws_caller_identity.current.account_id}"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "compute" {
  bucket                  = aws_s3_bucket.compute.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "sagemaker_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}

# The job's own bucket and logs, and pulling AWS's deep-learning container images.
data "aws_iam_policy_document" "sagemaker_access" {
  statement {
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.compute.arn}/*"]
  }
  statement {
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.compute.arn]
  }
  statement {
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogStreams"]
    resources = ["arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/sagemaker/*"]
  }
  statement {
    actions   = ["ecr:GetAuthorizationToken", "cloudwatch:PutMetricData"]
    resources = ["*"]
  }
  statement {
    actions   = ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer", "ecr:BatchCheckLayerAvailability"]
    resources = ["arn:aws:ecr:${var.aws_region}:763104351884:repository/*"]
  }
}

resource "aws_iam_role" "sagemaker" {
  name               = "sflad-sagemaker-role"
  assume_role_policy = data.aws_iam_policy_document.sagemaker_assume.json
}

resource "aws_iam_role_policy" "sagemaker" {
  name   = "compute"
  role   = aws_iam_role.sagemaker.id
  policy = data.aws_iam_policy_document.sagemaker_access.json
}
