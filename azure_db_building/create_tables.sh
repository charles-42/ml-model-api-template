#!/bin/bash

# Azure SQL Server credentials
server="DBServerNameOlistmodelapitemplate.database.windows.net"
database="olist"
username="adminuser"
password="eyJhbGciOiJIUzI1NiIsInR5cCI@^zdW%IiOiJhZG1pbiH3CxlTRDJj3RMKrY6B4x8"

# Path to your SQL script file
sqlScript="/Users/charles/Documents/pythonProject/data-model-template/azure_db_building/create_table.sql"

# Connect to Azure SQL Server and execute the SQL script
sqlcmd -S $server -d $database -U $username -P $password -i $sqlScript
