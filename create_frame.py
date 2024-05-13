import cv2
import os
import argparse

# Function to extract frames from video
def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Skip frames for the first 3 seconds
    cap.set(cv2.CAP_PROP_POS_MSEC, 3000)

    # Skip frames to capture one frame every 5 seconds
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save frame as PNG
        frame_path = os.path.join(output_folder, f"frame_{frame_count}.png")
        cv2.imwrite(frame_path, frame)

        # Increment frame count
        frame_count += 1

        # Jump to next frame
        cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 5000)  # Skip to next 5 seconds

    # Release the video capture object
    cap.release()

    return frame_count

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description='Inference on video frames using LLama AI.')
    parser.add_argument('video_file', type=str, help='Path to the input video file')

    # Parse arguments
    args = parser.parse_args()

    # Output folder for frames
    output_folder = 'frames'

    # Extract frames from video
    frame_count = extract_frames(args.video_file, output_folder)

if __name__ == "__main__":
    main()
