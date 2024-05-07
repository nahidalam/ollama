#!/bin/bash

# Log file
LOG_FILE="docker_run_log.txt"

# Function to log errors
log_error() {
    echo "$(date) - ERROR: $1" >> "$LOG_FILE"
}

# Pull the docker image
docker pull ollama/ollama >> "$LOG_FILE" 2>&1 || { log_error "Failed to pull the docker image"; exit 1; }

# Run the docker container
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama >> "$LOG_FILE" 2>&1 || { log_error "Failed to run the docker container"; exit 1; }

# Run the additional command
docker exec -it ollama ollama run llava-llama3 "describe this image: ./art.jpg" >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    log_error "Failed to execute the additional command"
    exit 1
fi

