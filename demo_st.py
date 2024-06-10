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
st.write("Upload motion alert images to generate text description")

# Directory selection
uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
# Save uploaded files to a temporary directory
temp_dir = "/Users/nahalam/Documents/code/ai/ollama/temp/"

if uploaded_files:
    prompt = st.text_input("Enter the prompt for the description:", value=prompt)
    if st.button("Generate Descriptions"):
        
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        image_paths = []
        for uploaded_file in uploaded_files:
            image_path = os.path.join(temp_dir, uploaded_file.name)
            print(temp_dir)
            print(uploaded_file.name)
            print(image_path)
            with open(image_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            image_paths.append(image_path)
        
        descriptions = get_image_descriptions(image_paths, prompt)
        print(descriptions)

        st.write("### Generated Descriptions")
        for image_path, description in descriptions:
            image = Image.open(image_path)
            st.image(image, caption=image_path)
            st.write(description)
else:
    st.write("No images uploaded yet.")

# Clean up temporary directory after execution
import shutil
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

