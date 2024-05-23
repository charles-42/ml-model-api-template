# execute chmod +x build_app_web_image.sh before

set -o allexport
source .env
set +o allexport

# Warning: you need to update the path ./app_web to the path of your dockerfile
docker build -t app_web:latest ./app_web

docker run -p 8000:8000 \
  -e TOKEN=$TOKEN \
  -e APP_NAME=$APP_NAME \
  app_web:latest
