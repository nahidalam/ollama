import gradio as gr
import os
import requests

# Default model
model = "moondream"

# Function to perform inference using Ollama
def perform_inference(image_path, prompt):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [image_path]
            }
        ]
    }
    response = requests.post(url, json=data)
    return response.json()

# Function to load images from a directory
def load_images_from_directory(directory):
    image_list = []
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            image_list.append(image_path)
    return image_list

# Function to handle image selection and prompt input
def handle_image_selection(image_path, prompt):
    default_prompt = "Analyze the motion detected in this image."
    prompt = prompt if prompt else default_prompt
    response = perform_inference(image_path, prompt)
    return response['content']

# Directory containing images
image_directory = "/Users/nahalam/Documents/code/ai/ollama/frames"

# Load images from the directory
image_paths = load_images_from_directory(image_directory)

# Create Gradio interface
'''
image_dropdown = gr.inputs.Dropdown(choices=image_paths, label="Select an Image")
prompt_textbox = gr.inputs.Textbox(label="Enter your prompt (optional)", default="")
output_textbox = gr.outputs.Textbox(label="Response")
'''
image_dropdown = gr.components.Dropdown(choices=image_paths, label="Select an Image")
prompt_textbox = gr.components.Textbox(label="Enter your prompt (optional)", default="")
output_textbox = gr.components.Textbox(label="Response")

iface = gr.Interface(
    fn=handle_image_selection,
    inputs=[image_dropdown, prompt_textbox],
    outputs=output_textbox,
    title="Motion Alert Text",
    description="Select an image and optionally enter a prompt to perform inference using Ollama. If no prompt is provided, a default prompt will be used."
)

# Launch the Gradio interface
iface.launch()

