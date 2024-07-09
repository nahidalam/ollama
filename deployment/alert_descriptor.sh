#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker and start the 'ollama' container."
    exit 1
fi

# Check if 'ollama' container is running
if ! docker ps | grep -q ollama; then
    echo "The 'ollama' Docker container is not running. Please start the container first."
    exit 1
fi

# Prompt to describe the person in the image
prompt='Describe the person in the image in 1 sentence, with upper and lower body clothing color and their environment. Do not describe gender or race'

# Determine the image file path
if [ $# -eq 0 ]; then
    image_path="./image.png"  # Default image path
else
    image_path="$1"  # Use user-provided image path
fi

# Check if the specified image file exists
if [ ! -f "$image_path" ]; then
    echo "Error: The specified image file '$image_path' does not exist."
    exit 1
fi

# Read image file as binary and encode to base64
image_base64=$(base64 < "$image_path" | tr -d '\n')

echo $image_base64

# Temp file to store JSON data
temp_json=$(mktemp /tmp/json.XXXXXX)

# Generate JSON data
cat > "$temp_json" <<EOF
{
  "model": "llava-llama3",
  "prompt": "$prompt",
  "stream": false,
  "images": ["$image_base64"]
}
EOF

# Curl command to interact with llava-llama3 model using --data-binary
curl -X POST http://localhost:11434/api/chat \
     -H "Content-Type: application/json" \
     --data-binary @"$temp_json"

# Cleanup temp file
rm "$temp_json"

echo "Done."
