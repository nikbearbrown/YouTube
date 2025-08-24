#!/usr/bin/env python3
import os
import cv2
import re

# Constants
SAMPLE_RATE = 111  # Save every 111th frame

def clean_filename(filename):
    """
    Clean a filename by:
    1. Replacing one or more spaces with a single underscore
    2. Removing non-alphanumeric characters
    
    Parameters:
        filename (str): The filename to clean.
        
    Returns:
        str: The cleaned filename.
    """
    # Replace one or more spaces with a single underscore
    cleaned = re.sub(r'\s+', '_', filename)
    # Remove any character that is not alphanumeric, underscore, or period
    cleaned = re.sub(r'[^\w\.]', '', cleaned)
    # Remove consecutive underscores
    cleaned = re.sub(r'_{2,}', '_', cleaned)
    return cleaned

def sample_frames(video_path):
    """
    Extract frames from a video at a fixed interval and save them as PNGs.
    
    Parameters:
        video_path (str): Path to the video file.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return
        
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    # Clean the video name for the output filename
    video_name = clean_filename(video_name)
    
    frame_count = 0
    saved_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:  # End of video
            break
            
        # Save every SAMPLE_RATE frame
        if frame_count % SAMPLE_RATE == 0:
            output_filename = f"{video_name}_frame_{frame_count:06}.png"
            cv2.imwrite(output_filename, frame)
            saved_count += 1
            
        frame_count += 1
        
    cap.release()
    print(f"Saved {saved_count} frames from {video_path}")

def process_videos_in_directory(directory):
    """
    Process all .mp4 files in the given directory.
    
    Parameters:
        directory (str): Path to the directory containing video files.
    """
    for file in os.listdir(directory):
        if file.lower().endswith(".mp4"):
            video_path = os.path.join(directory, file)
            print(f"Processing video: {video_path}")
            sample_frames(video_path)

if __name__ == "__main__":
    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")
    process_videos_in_directory(current_directory)