#!/bin/sh
echo "Commencing build and deployment"
docker build --platform linux/amd64 -t default-service-fastapi:latest .
echo "Build completed, tagging container"
docker tag default-service-fastapi europe-west3-docker.pkg.dev/firebase-svelte-381023/originations/default-service-fastapi
echo "Tag completed, pushing to google cloud repository"
docker push europe-west3-docker.pkg.dev/firebase-svelte-381023/originations/default-service-fastapi
echo "Push to GCR completed, deploying service"
gcloud run deploy default-service \
         --image europe-west3-docker.pkg.dev/firebase-svelte-381023/originations/default-service-fastapi \
         --region europe-west3 \
         --port 80 \
         --memory 4Gi
echo "!!!Deployment complete!!!"