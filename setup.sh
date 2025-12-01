#!/bin/bash

echo "Building Docker image..."
docker build -t esb1c-fake-api .

echo "Running Docker container..."
docker run -d --name esb1c-fake-api -p 9090:5000 esb1c-fake-api

echo "Container started. Access the API at http://localhost:9090"

timeout 30 bash -c 'while ! curl -s http://localhost:9090 > /dev/null 2>&1; do sleep 1; done' || echo "Timeout: API not available"

echo "Loading data..."
python scripts/load_data.py http://localhost:9090
