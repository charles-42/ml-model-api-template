// main.tf
provider "azurerm" {
  features {}
}

// Database module
module "database" {
  source              = "./database"
  resource_group_name = var.resource_group_name
  location            = var.location
  server_name         = var.server_name
  admin_username      = var.admin_username
  admin_password      = var.admin_password
  database_name       = var.database_name
}

