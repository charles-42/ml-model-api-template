# Load environment variables from .env file
set -o allexport
source .env
set +o allexport
#!/bin/bash

# # # Login
# # az login

# Create a new resource group
az group create --name $RESSOURCE_GROUP --location $LOCATION

# Create a new SQL server
az postgres server create\
    --name $SERVER_NAME\
    --resource-group $RESSOURCE_GROUP\
    --location $LOCATION\
    --admin-user $USERNAME\
    --admin-password $PASSWORD\
    --public all\
    --sku-name B_Gen5_1\
    --storage-size 5120

# Create a new SQL database
az postgres db create --resource-group $RESSOURCE_GROUP --server $SERVER_NAME --name $DATABASE 


# az postgres server show --resource-group $RESSOURCE_GROUP --name $SERVER_NAME