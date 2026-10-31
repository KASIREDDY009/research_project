output "apps" {
  description = "Per-application names and baseline settings, read by the evaluation scripts."
  value = {
    orders   = module.orders.app
    bookings = module.bookings.app
  }
}

output "compute" {
  description = "SageMaker bucket and role."
  value = {
    bucket   = aws_s3_bucket.compute.bucket
    role_arn = aws_iam_role.sagemaker.arn
    region   = var.aws_region
  }
}
