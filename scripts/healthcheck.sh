#!/bin/bash
set -e

SERVICES=(
  "http://localhost:8000/health"
  "http://localhost:8001/health"
  "http://localhost:8002/health"
  "http://localhost:8003/health"
  "http://localhost:8004/health"
  "http://localhost:8005/health"
  "http://localhost:8006/health"
  "http://localhost:8007/health"
  "http://localhost:8008/health"
  "http://localhost:8009/health"
)

echo "Verifying NovaCommerce Microservice Cluster Health..."
for URL in "${SERVICES[@]}"; do
  echo -n "Checking $URL ... "
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || echo "FAILED")
  if [ "$STATUS" == "200" ]; then
    echo "OK (200)"
  else
    echo "DEGRADED ($STATUS)"
  fi
done
