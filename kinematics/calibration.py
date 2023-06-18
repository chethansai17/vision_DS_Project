import cv2
import numpy as np

# Define the object points in 3D space
object_points = np.array([
    (0, 0, 0),
    (0, 10, 0),
    (10, 10, 0),
    (10, 0, 0)
], dtype=np.float32)

# Define the image points in 2D space
image_points = np.array([
    (200, 200),
    (250, 150),
    (300, 200),
    (250, 250)
], dtype=np.float32)

# Define the size of the checkerboard pattern used for calibration
pattern_size = (4, 4)

# Define a list to store the object points and image points for each image used for calibration
object_points_list = []
image_points_list = []

# Read the calibration images and find the checkerboard corners
for i in range(1, 21):
    # Load the calibration image
    img = cv2.imread(f'calibration_images/calibration{i}.jpg')

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the checkerboard corners
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if ret:
        # Add the object points and image points to the lists
        object_points_list.append(object_points)
        image_points_list.append(corners)

# Perform camera calibration to obtain the camera matrix and distortion coefficients
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    object_points_list, image_points_list, gray.shape[::-1], None, None)

# Define the object point to convert to real-world coordinates
obj_point = np.array([(5, 5, 0)], dtype=np.float32)

# Project the object point onto the image plane
img_point, _ = cv2.projectPoints(obj_point, np.array([0, 0, 0]), np.array([0, 0, 0]), camera_matrix, dist_coeffs)

# Print the image point and the corresponding real-world coordinates
print(f'Image point: {img_point[0][0]}')
print(f'Real-world coordinates: {obj_point[0]}')
