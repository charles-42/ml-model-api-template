set -o allexport
source .env
set +o allexport

az account set --subscription $SUBSCRIPTION_ID

az ad sp create-for-rbac \
    --name myApp \
    --role contributor \
    --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESSOURCE_GROUP \
    --json-auth
       