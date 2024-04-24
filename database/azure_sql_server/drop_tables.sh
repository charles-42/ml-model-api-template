#!/bin/bash

# Azure SQL Server credentials
server="DBOlistModelApiTemplate.database.windows.net"
database="olist"
username="adminuser"
password="eyJhbGciOiJIUzI1NiIsInR5cCI@^zdW%IiOiJhZG1pbiH3CxlTRDJj3RMKrY6B4x8"

# Connect to Azure SQL Server and execute the SQL script
sqlcmd -S $server -d $database -U $username -P $password -Q "DROP TABLE Reviews;" #; DROP TABLE Orders ;"

