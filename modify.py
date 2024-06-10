import streamlit as st
import os
from PIL import Image
import ollama

prompt = 'Describe the person in the image in 1 sentence, with upper and lower body clothing color and their environment. Do not describe gender or race'

def get_image_descriptions(image_paths, prompt):
    descriptions = []
    for image_path in image_paths:
        image_file_name = os.path.basename(image_path)
        with open(image_path, 'rb') as img_file:
            res = ollama.chat(
                model="llava-llama3",
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [img_file.read()]
                    }
                ]
            )
            description = res['message']['content']
            descriptions.append((image_path, description))
    return descriptions

# Streamlit app layout
st.title("Motion Alert Text")
st.write("Select images to generate text description")

# Directory with images
image_dir = "/Users/nahalam/Documents/code/ai/ollama/frames/"

# List all images in the directory
all_images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

# Show available images with checkboxes
selected_images = []
st.write("### Available Images")
for image_path in all_images:
    image = Image.open(image_path)
    image_name = os.path.basename(image_path)
    if st.checkbox(image_name, key=image_path):
        selected_images.append(image_path)
    st.image(image, caption=image_name, width=150)

# Drag and drop file uploader
uploaded_files = st.file_uploader("Or drag and drop images here", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files:
    # Save uploaded files to the temporary directory
    for uploaded_file in uploaded_files:
        image_path = os.path.join(image_dir, uploaded_file.name)
        with open(image_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        selected_images.append(image_path)

if selected_images:
    prompt = st.text_input("Enter the prompt for the description:", value=prompt)
    if st.button("Generate Descriptions"):
        descriptions = get_image_descriptions(selected_images, prompt)

        st.write("### Generated Descriptions")
        for image_path, description in descriptions:
            image = Image.open(image_path)
            st.image(image, caption=os.path.basename(image_path))
            st.write(description)
else:
    st.write("No images selected yet.")
