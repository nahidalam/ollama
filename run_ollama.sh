#!/bin/bash

# Pull the docker image
docker pull ollama/ollama

# Run the docker container
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

