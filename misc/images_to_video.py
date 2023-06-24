import os
import cv2
import numpy as np

folder_path = "./images/7"

# Read image file names
image_files = [f for f in os.listdir(folder_path) if f.endswith(".png") or f.endswith(".jpg")]

# Sort image files by timestamp
image_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

# Calculate FPS
timestamps = [int(os.path.splitext(f)[0]) for f in image_files]
time_diffs = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
avg_time_diff = np.mean(time_diffs)
fps = 1000 / avg_time_diff
print("FPS: ", fps)

# Read first image to get height, width and layers
first_image = cv2.imread(os.path.join(folder_path, image_files[0]))
height, width, layers = first_image.shape

# Define output video file
output_video_file = os.path.join(folder_path, "video_" + str(height) + ".avi")

# Create video writer
video_writer = cv2.VideoWriter(output_video_file, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

# Write images to video
for image_file in image_files:
    image = cv2.imread(os.path.join(folder_path, image_file))
    video_writer.write(image)

video_writer.release()