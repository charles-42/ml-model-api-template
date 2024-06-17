set -o allexport
source .env
set +o allexport

# This is suppose to be the way to create app credentials
az account set --subscription $SUBSCRIPTION_ID

# find a unique name if you have the error: not enough privilege
az ad sp create-for-rbac \
    --name myApp \ 
    --role contributor \
    --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESSOURCE_GROUP \
    --json-auth


# AUTRE SOLUTION SI LA PREMIERE NE MARCHE PAS

# APP_NAME="Github_Login_$(date +%s)"

# EXISTING_APP_ID=$(az ad app list --display-name $APP_NAME --query "[0].appId" -o tsv)
# if [ -z "$EXISTING_APP_ID" ]; then
#     echo "Application does not exist, creating new application"
#     APP_JSON=$(az ad app create --display-name "$APP_NAME")
#     APP_ID=$(echo "$APP_JSON" | jq -r '.appId')
# else
#     echo "Application already exists, using existing appId"
#     APP_ID=$EXISTING_APP_ID
# fi
# echo "APP_ID=$APP_ID"
# echo "APP_NAME=$APP_NAME"


# az ad app update --id $APP_ID  --set groupMembershipClaims=All

# az ad sp create --id $APP_ID

# az account set --subscription $SUBSCRIPTION_ID

# az role assignment create --assignee $APP_ID --role Contributor --scope subscriptions/$SUBSCRIPTION_ID

# az ad sp credential reset --id $APP_ID --append --years 2

