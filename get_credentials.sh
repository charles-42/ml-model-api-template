set -o allexport
source .env
set +o allexport

# This is suppose to be the way to create app credentials
# az account set --subscription $SUBSCRIPTION_ID

# az ad sp create-for-rbac \
#     --name myApp \
#     --role contributor \
#     --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESSOURCE_GROUP \
#     --json-auth


# Create the application and capture the output in JSON format
APP_JSON=$(az ad app create --display-name "Github_Login")

# Extract the appId using jq and store it in a variable
APP_ID=$(echo $APP_JSON | jq -r '.appId')

az ad app update --id $APP_ID  --set groupMembershipClaims=All

az ad sp create --id $APP_ID

az account set --subscription $SUBSCRIPTION_ID

az role assignment create --assignee $APP_ID --role Contributor --scope subscriptions/$SUBSCRIPTION_ID

az ad sp credential reset --id $APP_ID --append --years 2