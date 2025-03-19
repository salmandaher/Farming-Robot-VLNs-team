import numpy as np
import cv2

# Given data
camera_matrix = np.array([[699.394139, 0, 335.3583577],
                          [0, 658.05082595, 230.4636284],
                          [0, 0, 1]])
dist_coeffs = np.array([1.21571464e-01, -9.09319924e-01, -6.16281440e-03, 1.58134556e-03, 2.59246739e+00])

rotation_vector = np.array([-0.05989835, 0.75451456, 3.05180379])
translation_vector = np.array([4.73363144, 1.93273359, 13.5637211])
pixel_points = np.array([[146,71], [236,67], [322,66], [408,67], [493,64],
                         [133,160], [228,160], [320,160], [420,156], [508,160],
                         [114,273], [219,271], [325,267], [416,265], [523,261],
                         [101,402], [212,400], [327,392], [437,388], [543,384]])

world_points = np.array([[-14, 28], [-7, 28], [0, 28], [7, 28], [14, 28],
                         [-14, 21], [-7, 21], [0, 21], [7, 21], [14, 21],
                         [-14, 14], [-7, 14], [0, 14], [7, 14], [14, 14],
                         [-14, 7], [-7, 7], [0, 7], [7, 7], [14, 7]])

# Point to be converted
pixel_point_to_convert = np.array([178, 219], dtype=np.float32)

# Step 1: Undistort the pixel coordinates
undistorted_points = cv2.undistortPoints(np.expand_dims(pixel_point_to_convert, axis=0), camera_matrix, dist_coeffs, P=camera_matrix)

# Step 2: Convert to normalized image coordinates
normalized_image_point = undistorted_points[0][0]

# Step 3: Calculate the 3D point in the camera coordinate system
# Z is unknown, but we are on a plane z=0 in world coordinates, we need to transform into the camera system.
# Since all points are on the same plane z=0, we use homography estimation

# Calculate homography using the known points
homography_matrix, _ = cv2.findHomography(pixel_points, world_points)

# Convert the pixel point to homogenous coordinates
pixel_point_homogeneous = np.append(pixel_point_to_convert, 1).reshape(3, 1)

# Transform the pixel point to the world coordinates using the homography matrix
world_point_homogeneous = np.dot(homography_matrix, pixel_point_homogeneous)

# Normalize to get the world coordinates
world_point = world_point_homogeneous / world_point_homogeneous[2]

print("The real-world coordinates are:", world_point[:2].flatten())
print(world_point)