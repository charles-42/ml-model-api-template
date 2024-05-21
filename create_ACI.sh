set -o allexport
source .env
set +o allexport

az container create \
            --resource-group $RESSOURCE_GROUP \
            --name apimodeletemplate3 \
            --image $DOCKERHUB_USERNAME/api_modele:latest \
            --cpu 1 \
            --memory 1 \
            --ip-address public \
            --ports 80 8000 \
            --environment-variables \
              "SUBSCRIPTION_ID"=$SUBSCRIPTION_ID \
              "RESSOURCE_GROUP"=$RESSOURCE_GROUP \
              "WORKSPACE_NAME"=$WORKSPACE_NAME \
              "SERVER"=$SERVER \
              "DATABASE"=$DATABASE \
              "POSTGRES_USER"=$POSTGRES_USER \
              "PASSWORD"=$PASSWORD \
              "SECRET_KEY"=$SECRET_KEY