#!/bin/bash

echo "Applying Kubernetes configurations..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

echo "Deployment complete!"

