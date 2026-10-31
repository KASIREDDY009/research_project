# App A (orders) and App B (bookings): the same AWS services, different business logic and log vocabulary.
module "orders" {
  source              = "./modules/app"
  name                = "sflad-orders-api"
  source_dir          = "${path.module}/../../src/apps/orders"
  table_name          = "sflad-orders"
  table_key           = "order_id"
  resource            = "orders"
  reference_data_size = var.orders_reference_data_size
  memory_size         = var.memory_size
  timeout_seconds     = var.timeout_seconds
  log_level           = var.log_level
  log_retention_days  = var.log_retention_days
}

module "bookings" {
  source              = "./modules/app"
  name                = "sflad-bookings-api"
  source_dir          = "${path.module}/../../src/apps/bookings"
  table_name          = "sflad-bookings"
  table_key           = "booking_id"
  resource            = "bookings"
  reference_data_size = var.bookings_reference_data_size
  memory_size         = var.memory_size
  timeout_seconds     = var.timeout_seconds
  log_level           = var.log_level
  log_retention_days  = var.log_retention_days
}
