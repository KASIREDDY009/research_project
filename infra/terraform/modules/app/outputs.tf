output "app" {
  description = "Everything the evaluation needs to drive, fault and restore this application."
  value = {
    function_name   = aws_lambda_function.this.function_name
    role_arn        = aws_iam_role.this.arn
    logs_role_arn   = aws_iam_role.logs_only.arn
    table_name      = aws_dynamodb_table.this.name
    table_key       = var.table_key
    resource        = var.resource
    log_group       = aws_cloudwatch_log_group.this.name
    memory_size     = aws_lambda_function.this.memory_size
    timeout_seconds = aws_lambda_function.this.timeout
    environment     = aws_lambda_function.this.environment[0].variables
  }
}
