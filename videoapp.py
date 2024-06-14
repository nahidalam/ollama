import streamlit as st
import cv2
import os
import tempfile
from PIL import Image
import ollama

def extract_frame(video_path, timestamp):
    cap = cv2.VideoCapture(video_path)
    
    # Set the video frame to the specified timestamp
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    
    success, frame = cap.read()
    
    if success:
        return frame
    else:
        return None

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

st.title("Motion Alert Descriptor")

uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_video is not None:
    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video_file:
        tmp_video_file.write(uploaded_video.read())
        tmp_video_path = tmp_video_file.name

    # Load the video using OpenCV to get the total duration
    cap = cv2.VideoCapture(tmp_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    # Use streamlit-player to play the video
    st.video(tmp_video_path)

    # Slider to select the timestamp
    timestamp = st.slider("Select timestamp (in seconds)", 0, int(duration), 0, 1)

    if st.button("Extract Frame"):
        frame = extract_frame(tmp_video_path, timestamp)
        
        if frame is not None:
            st.image(frame, channels="BGR")

            # Ensure the 'temp_frame' directory exists
            temp_frame_dir = os.path.join(os.getcwd(), 'temp_frame')
            os.makedirs(temp_frame_dir, exist_ok=True)

            # Save the frame to the 'temp_frame' directory
            frame_path = os.path.join(temp_frame_dir, 'frame.jpg')
            cv2.imwrite(frame_path, frame)
            
            # Define the prompt
            prompt = 'Describe the person in the image in 1 sentence, with upper and lower body clothing color and their environment. Do not describe gender or race'
            
            # Get image descriptions
            descriptions = get_image_descriptions([frame_path], prompt)
            
            for image_path, description in descriptions:
                st.write(f"Motion Alert Text: {description}")
        else:
            st.write("Could not extract frame. Please check the timestamp.")
