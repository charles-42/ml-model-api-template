set -o allexport
source .env
set +o allexport

docker build -t model_api:latest ./api

docker run -p 8000:8000 \
  -e SUBSCRIPTION_ID=$SUBSCRIPTION_ID \
  -e RESSOURCE_GROUP=$RESSOURCE_GROUP \
  -e WORKSPACE_NAME=$WORKSPACE_NAME \
  -e SERVER=$SERVER \
  -e DATABASE=$DATABASE \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e PASSWORD=$PASSWORD \
  -e SECRET_KEY=$SECRET_KEY \
  model_api:latest
