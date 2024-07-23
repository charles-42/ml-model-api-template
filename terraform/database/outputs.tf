output "server_name" {
  value = azurerm_postgresql_server.main.name
}

output "database_name" {
  value = azurerm_postgresql_database.main.name
}
