#!/bin/bash

container_name="esb1c-fake-api"
image_name="2405964484/${container_name}"
server_url="http://localhost:9090"

docker stop ${container_name}
docker rm ${container_name} 
# docker rmi ${image_name}

echo "Building Docker image..."
docker build -t ${image_name} .

echo "Running Docker container..."
docker run -d --name esb1c-fake-api -p 9090:5000 ${image_name}

echo "Container started. Access the API at ${server_url}"

timeout 30 bash -c "while ! curl -s ${server_url} > /dev/null 2>&1; do sleep 1; done" || echo "Timeout: API not available"

echo "Loading data..."
python scripts/load_default_data.py ${server_url}
