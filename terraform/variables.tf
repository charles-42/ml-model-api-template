variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The location of the resource group"
  type        = string
}

variable "server_name" {
  description = "The name of the PostgreSQL server"
  type        = string
}

variable "admin_username" {
  description = "The admin username for PostgreSQL server"
  type        = string
}

variable "admin_password" {
  description = "The admin password for PostgreSQL server"
  type        = string
}

variable "database_name" {
  description = "The name of the PostgreSQL database"
  type        = string
}