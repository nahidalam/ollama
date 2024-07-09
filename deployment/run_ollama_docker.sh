#!/bin/bash

# reference: https://hub.docker.com/r/ollama/ollama
# TODO: check if there is any ollama docker already. and check if it works. If not stop and remove that docker and run this
# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to start Docker service (if not already running)
start_docker_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux/Ubuntu
        if sudo systemctl is-active --quiet docker; then
            echo "Docker service is already running."
        else
            echo "Starting Docker service..."
            sudo systemctl start docker
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command_exists docker; then
            echo "Docker is not installed. Please install Docker for macOS."
            exit 1
        fi
        echo "Docker daemon should already be running on macOS."
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
        # Windows
        echo "Windows platform detected. Docker should be running."
    else
        echo "Unsupported OS. Please run this script on Linux, macOS, or Windows with Docker installed."
        exit 1
    fi
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker."
    exit 1
fi

# Check Docker daemon status and start if necessary
start_docker_service

# Run the Docker container
echo "Running the Ollama Docker container..."
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Wait for the Docker container to be fully up and running
echo "Waiting for the Docker container to be fully up and running..."
sleep 10

# Pull the llava-llama3 model using ollama
echo "Pulling the llava-llama3 model using ollama..."
docker exec ollama ollama pull llava-llama3

echo "Done."
