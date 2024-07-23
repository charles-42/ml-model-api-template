resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_postgresql_server" "main" {
  name                = var.server_name
  location            = var.location
  resource_group_name = var.resource_group_name
  administrator_login = var.admin_username
  administrator_login_password = var.admin_password
  sku_name            = "B_Gen5_1"
  storage_mb          = 5120
  version             = "11"
  ssl_enforcement_enabled = true
}

resource "azurerm_postgresql_database" "main" {
  name                = var.database_name
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_postgresql_server.main.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}