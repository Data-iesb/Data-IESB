#!/bin/bash

# Usage: ./toggle-psd.sh [0|1]
# 0 = OFF (delete resources)
# 1 = ON (apply resources)

NAMESPACE="default"

if [ "$1" != "0" ] && [ "$1" != "1" ]; then
  echo "❌ Invalid argument. Use 0 to turn OFF, 1 to turn ON."
  exit 1
fi

if [ "$1" == "1" ]; then
  echo "🚀 Turning ON resources (apply manifests)..."
  kubectl apply -f "deployment.yaml" -n "$NAMESPACE"
  kubectl apply -f "service.yaml" -n "$NAMESPACE"
  kubectl apply -f "ingress.yaml" -n "$NAMESPACE"
  echo "✅ All resources turned ON."
else
  echo "🛑 Turning OFF resources (delete manifests)..."
  kubectl delete -f "ingress.yaml" -n "$NAMESPACE" --ignore-not-found
  kubectl delete -f "service.yaml" -n "$NAMESPACE" --ignore-not-found
  kubectl delete -f "deployment.yaml" -n "$NAMESPACE" --ignore-not-found
  echo "✅ All resources turned OFF."
fi

