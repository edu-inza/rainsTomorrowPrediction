#!/bin/bash

# get repository
echo "Clone git repository"
git clone https://github.com/edu-inza/rainsTomorrowPrediction.git

# Unit tests with docker
echo "API : build docker image"
cd $PWD/rainsTomorrowPrediction/api
docker image build . -t einza/rains_tomorrow_api

echo "TU authorization : build docker image"
cd ../TU_authorization
docker image build . -t einza/tu_authorization

echo "TU_prediction : build docker image"
cd ../TU_prediction
docker image build . -t einza/tu_prediction

echo "Execute unit tests : docker compose up"
cd ..
docker-compose up -d

sleep 10

echo "Docker compose down"
docker-compose down

# Deploy in kubernetes
echo "Deploy api in kubernetes"
cd ./k8s
kubectl create -f k8s-api-deployment.yml
kubectl get deployment

echo "Deploy ClusterIP service in kubernetes"
kubectl create -f k8s-service.yml
kubectl get service

echo "Deploy ingress in kubernetes"
kubectl create -f k8s-ingress.yml
kubectl get ingress