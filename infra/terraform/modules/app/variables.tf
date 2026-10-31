variable "name" {
  description = "Lambda function name."
  type        = string
}

variable "source_dir" {
  description = "Directory holding the function's handler.py."
  type        = string
}

variable "table_name" {
  description = "DynamoDB table name."
  type        = string
}

variable "table_key" {
  description = "Hash key of the table, also the API path parameter."
  type        = string
}

variable "resource" {
  description = "API collection path part (orders, bookings)."
  type        = string
}

variable "reference_data_size" {
  description = "Entries in the function's in-memory reference data (its memory working set)."
  type        = number
}

variable "memory_size" {
  description = "Lambda memory in MB."
  type        = number
}

variable "timeout_seconds" {
  description = "Lambda timeout in seconds."
  type        = number
}

variable "log_level" {
  description = "Lambda LOG_LEVEL environment variable."
  type        = string
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention for the function's log group."
  type        = number
}
