

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

#az login

az account set --subscription $SUBSCRIPTION_ID

az ml workspace create \
    --name $WORKSPACE_NAME \
    --resource-group $RESSOURCE_GROUP \
    --location $LOCATION

az configure --defaults workspace=$WORKSPACE_NAME group=$RESSOURCE_GROUP location=$LOCATION 

az ml workspace show --query mlflow_tracking_uri

