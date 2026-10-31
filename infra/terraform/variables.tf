variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "eu-west-1"
}

variable "memory_size" {
  description = "Lambda memory in MB for both applications."
  type        = number
  default     = 512
}

variable "timeout_seconds" {
  description = "Lambda timeout in seconds for both applications."
  type        = number
  default     = 10
}

variable "log_level" {
  description = "Lambda LOG_LEVEL environment variable."
  type        = string
  default     = "INFO"
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention for the Lambda log groups."
  type        = number
  default     = 14
}

variable "orders_reference_data_size" {
  description = "Products in the orders catalogue (App A's in-memory working set)."
  type        = number
  default     = 400000
}

variable "bookings_reference_data_size" {
  description = "Venues in the bookings calendar (App B's in-memory working set)."
  type        = number
  default     = 700000
}
