# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

az postgres db delete \
--resource-group $RESSOURCE_GROUP \
--server-name $SERVER_NAME \
--name $DATABASE

az postgres server delete \
--resource-group $RESSOURCE_GROUP \
--name $SERVER_NAME

az ml workspace delete \
--resource-group $RESSOURCE_GROUP \
--name $WORKSPACE_NAME

az group delete \
--name $RESSOURCE_GROUP