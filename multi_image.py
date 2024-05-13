import os
import ollama

# Pull the llava-llama3 model
ollama.pull('llava-llama3')

# Directory containing images
image_dir = './frames'  # Specify the directory containing the images

# List of images (JPG and PNG)
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]

# Initial prompt
prompt = 'Describe this image:'

# Accumulator for context
context = ''

# Loop over each image
for image_path in image_paths:
    # Perform inference
    res = ollama.chat(
        model="llava-llama3",
        messages=[
            {
                'role': 'user',
                'content': f'Please describe the image given the context {context}',
                'images': [image_path]
            }
        ]
    )

    # Print the text output
    print("Output:")
    print(res['message']['content'])
    print("****************")

    # Update context
    context += res['message']['content'] + '\n'

    # Update prompt for the next iteration
    prompt = res['message']['content']
    print("current prompt:", prompt)
    print("---------------")