# One serverless application: Lambda -> DynamoDB, with its own log group and role.
data "archive_file" "code" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.root}/build/${var.name}.zip"
  excludes    = ["__pycache__", "*.pyc", ".DS_Store"]
}

resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = var.table_key

  attribute {
    name = var.table_key
    type = "S"
  }
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = var.log_retention_days
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Logs for this function; items in tables whose name starts with this application's table name.
data "aws_iam_policy_document" "access" {
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.this.arn}:*"]
  }
  statement {
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem"]
    resources = ["${aws_dynamodb_table.this.arn}*"]
  }
}

resource "aws_iam_role" "this" {
  name               = "${var.name}-role"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_iam_role_policy" "access" {
  name   = "access"
  role   = aws_iam_role.this.id
  policy = data.aws_iam_policy_document.access.json
}

# A role that may only write logs: running the function under it is the permission fault.
data "aws_iam_policy_document" "logs_only" {
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.this.arn}:*"]
  }
}

resource "aws_iam_role" "logs_only" {
  name               = "${var.name}-logs-role"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_iam_role_policy" "logs_only" {
  name   = "logs-only"
  role   = aws_iam_role.logs_only.id
  policy = data.aws_iam_policy_document.logs_only.json
}

resource "aws_lambda_function" "this" {
  function_name    = var.name
  role             = aws_iam_role.this.arn
  handler          = "handler.handler"
  runtime          = "python3.12"
  memory_size      = var.memory_size
  timeout          = var.timeout_seconds
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256

  environment {
    variables = {
      TABLE_NAME          = var.table_name
      LOG_LEVEL           = var.log_level
      REFERENCE_DATA_SIZE = tostring(var.reference_data_size)
      INJECTED_DELAY_MS   = "0"
    }
  }

  depends_on = [aws_cloudwatch_log_group.this, aws_iam_role_policy.access]
}
