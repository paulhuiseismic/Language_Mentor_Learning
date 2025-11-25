#!/bin/bash
echo "========================================="
echo "Build completed successfully!"
echo "========================================="
echo ""

fi
    echo "Remove container: docker rm language-mentor-app"
    echo "Stop container: docker stop language-mentor-app"
    echo "View logs: docker logs -f language-mentor-app"
    echo ""
    echo "Access the application at: http://localhost:7860"
    echo "Container started successfully!"
    echo ""

        ${FULL_IMAGE_NAME}
        -v $(pwd)/logs:/app/logs \
        --env-file .env \
        -p 7860:7860 \
        --name language-mentor-app \
    docker run -d \

    fi
        echo "Please edit .env with your Azure OpenAI credentials before the container can work properly."
        cp .env.example .env
        echo "Warning: .env file not found. Copying from .env.example..."
    if [ ! -f .env ]; then
    # Check if .env file exists

    echo "Step 4: Starting container..."
then
if [[ $REPLY =~ ^[Yy]$ ]]
echo
read -p "Start the container? (y/n) " -n 1 -r
echo ""
# Optional: Start the container

fi
    echo "Tests completed!"
    docker build --target testing -t ${IMAGE_NAME}:test .
    echo "Step 3: Running tests in container..."
then
if [[ $REPLY =~ ^[Yy]$ ]]
echo
read -p "Run tests in container? (y/n) " -n 1 -r
echo ""
# Optional: Run tests in container

docker images | grep ${IMAGE_NAME}
echo "Step 2: Image built successfully!"
echo ""

docker build -t ${FULL_IMAGE_NAME} .
echo "Step 1: Building Docker image..."
# Build the image

echo ""
echo "Building image: ${FULL_IMAGE_NAME}"
echo ""

FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"
TAG="${1:-latest}"
IMAGE_NAME="language-mentor"
# Configuration

echo "========================================="
echo "Language Mentor - Docker Build Script"
echo "========================================="

set -e

# Build and test Docker image for Language Mentor

