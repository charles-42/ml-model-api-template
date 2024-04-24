#!/bin/bash

# Set variables for resource group, server name, and database name
resourceGroupName="BENIAC_data_api_olist"
location="francecentral"  # e.g., "eastus"
serverName="DBServerNameOlistmodelapitemplate"
databaseName="olist"
username="adminuser"
password='eyJhbGciOiJIUzI1NiIsInR5cCI@^zdW%IiOiJhZG1pbiH3CxlTRDJj3RMKrY6B4x8'

# # Login
# az login

# Create a new resource group
az group create --name $resourceGroupName --location $location

# Create a new SQL server
az sql server create --name $serverName --resource-group $resourceGroupName --location $location --admin-user $username --admin-password $password --enable-public-network true

# Allow Azure services to access the server
az sql server firewall-rule create --resource-group $resourceGroupName --server $serverName --name "AllowAzureServices" --start-ip-address "0.0.0.0" --end-ip-address "255.255.255.255"

# Create a new SQL database
az sql db create --resource-group $resourceGroupName --server $serverName --name $databaseName --service-objective Basic
