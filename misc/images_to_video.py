# How to use:
# $ python images_to_video.py <folder_path>
# <folder_path> must contain images with names like 0.png, 125.png, 398.png with the timestamp in milliseconds as the name

import os
import cv2 # $ pip install opencv-python opencv-python-headless
import numpy as np
import sys

folder_path = sys.argv[1]

# Read image file names
image_files = [f for f in os.listdir(folder_path) if f.endswith(".png") or f.endswith(".jpg")]

# Sort image files by timestamp
image_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

# Calculate FPS
timestamps = [int(os.path.splitext(f)[0]) for f in image_files]
time_diffs = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
avg_time_diff = np.mean(time_diffs)
fps = 1000 / avg_time_diff
print("Max time diff: ", np.max(time_diffs))
print("Min time diff: ", np.min(time_diffs))
print("Avg time diff: ", avg_time_diff)
print("Avg FPS: ", fps)


# override FPS
fps = 20

# Read first image to get height, width and layers
first_image = cv2.imread(os.path.join(folder_path, image_files[0]))
height, width, layers = first_image.shape

# Define output video file
output_video_file = os.path.join(folder_path, "video_" + str(height) + ".avi")

# Create video writer
video_writer = cv2.VideoWriter(output_video_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

millisecond_counter = int(os.path.splitext(image_files[0])[0])

# Write images to video
for image_file in image_files:
    image = cv2.imread(os.path.join(folder_path, image_file))
    while millisecond_counter <= int(os.path.splitext(image_file)[0]):
        video_writer.write(image)
        millisecond_counter += 1000 / fps

video_writer.release()
