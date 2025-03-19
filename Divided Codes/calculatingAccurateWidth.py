import cv2
import numpy as np
import math

camera_matrix = np.array([[1.57106039e+03, 0.00000000e+00, 9.05651746e+02],
                          [0.00000000e+00, 1.72561610e+03, 4.72610176e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist_coeffs = np.array([0.08856508, -0.67754484, -0.00266143, -0.00542227, 1.3737949])

rotation_vector = np.array([-0.91701443, 0.04130337, -0.03490848])
translation_vector = np.array([-3.70130181, 0.94605119, 24.3247255])

pixel_points = np.array([[257, 92], [348, 87], [439, 81], [530, 77], [622, 69], 
                         [244,154], [342,150], [441,146], [545,137], [641,134],
                         [233,232], [341,228], [449,219], [557,211], [664,207],
                         [216,314], [333,310], [452,305], [566,300], [685,295],
                         [193,427], [328,419], [457,414], [586,406], [717,402]])

world_points = np.array([[-14, 35], [-7, 35], [0, 35], [7, 35], [14, 35],
                         [-14, 28], [-7, 28], [0, 28], [7, 28], [14, 28],
                         [-14, 21], [-7, 21], [0, 21], [7, 21], [14, 21],
                         [-14, 14], [-7, 14], [0, 14], [7, 14], [14, 14],
                         [-14, 7 ], [-7, 7 ], [0, 7 ], [7, 7 ], [14, 7 ]])

img = cv2.imread('C:/Users/lightdsy/Desktop/mws/pythoon/image_for_cali/gren3.jpg')
img = cv2.resize(img, None, fx= 0.5, fy= 0.5, interpolation= cv2.INTER_LINEAR)
green_copy = img.copy()
hsv_image = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lowgreen = np.array([63,76,61])
highgreen = np.array([99,227,127])

green_mask=cv2.inRange(hsv_image,lowgreen,highgreen)

green_contours, hierarchy = cv2.findContours(image=green_mask, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)

contours_g = sorted(green_contours, key=cv2.contourArea, reverse=True)[:1]

starting=[0,0,0,0]
ending=[0,0,0,0]

top_left = (float('inf'), float('inf'))
top_right = (-float('inf'), float('inf'))
bottom_left = (float('inf'), -float('inf'))
bottom_right = (-float('inf'), -float('inf'))

for contour in contours_g:
    for point in contour:
        x, y = point[0]
        if x + y < sum(top_left):
            top_left = (x, y)
        if x - y > top_right[0] - top_right[1]:
            top_right = (x, y)
        if x - y < bottom_left[0] - bottom_left[1]:
            bottom_left = (x, y)
        if x + y > sum(bottom_right):
            bottom_right = (x, y)

    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
cv2.circle(green_copy, top_left, 5, (0, 0, 255), -1)
cv2.circle(green_copy, top_right, 5, (0, 0, 255), -1)
cv2.circle(green_copy, bottom_left, 5, (0, 0, 255), -1)
cv2.circle(green_copy, bottom_right, 5, (0, 0, 255), -1)

cv2.circle(green_copy, (cX, cY), 5, (0, 0, 255), -1)
cv2.drawContours(image=green_copy, contours=contours_g, contourIdx=-1, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

# Point to be converted
pixel_point_to_convert_t1 = np.array([top_left[0], top_left[1]], dtype=np.float32)
pixel_point_to_convert_t2 = np.array([top_right[0], top_right[1]], dtype=np.float32) 

pixel_point_to_convert_b1 = np.array([bottom_left[0], bottom_left[1]], dtype=np.float32)
pixel_point_to_convert_b2 = np.array([bottom_right[0], bottom_right[1]], dtype=np.float32) 

undistorted_points_t1 = cv2.undistortPoints(np.expand_dims(pixel_point_to_convert_t1, axis=0), camera_matrix, dist_coeffs, P=camera_matrix)
undistorted_points_t2 = cv2.undistortPoints(np.expand_dims(pixel_point_to_convert_t2, axis=0), camera_matrix, dist_coeffs, P=camera_matrix)

undistorted_points_b1 = cv2.undistortPoints(np.expand_dims(pixel_point_to_convert_b1, axis=0), camera_matrix, dist_coeffs, P=camera_matrix)
undistorted_points_b2 = cv2.undistortPoints(np.expand_dims(pixel_point_to_convert_b2, axis=0), camera_matrix, dist_coeffs, P=camera_matrix)

# Step 2: Convert to normalized image coordinates
normalized_image_point_t1 = undistorted_points_t1[0][0]
normalized_image_point_t2 = undistorted_points_t2[0][0]

normalized_image_point_b1 = undistorted_points_b1[0][0]
normalized_image_point_b2 = undistorted_points_b2[0][0]
# Step 3: Calculate the 3D point in the camera coordinate system
# Z is unknown, but we are on a plane z=0 in world coordinates, we need to transform into the camera system.
# Since all points are on the same plane z=0, we use homography estimation

# Calculate homography using the known points
homography_matrix, _ = cv2.findHomography(pixel_points, world_points)

# Convert the pixel point to homogenous coordinates
pixel_point_homogeneous_t1 = np.append(pixel_point_to_convert_t1, 1).reshape(3, 1)
pixel_point_homogeneous_t2 = np.append(pixel_point_to_convert_t2, 1).reshape(3, 1)

pixel_point_homogeneous_b1 = np.append(pixel_point_to_convert_b1, 1).reshape(3, 1)
pixel_point_homogeneous_b2 = np.append(pixel_point_to_convert_b2, 1).reshape(3, 1)
# Transform the pixel point to the world coordinates using the homography matrix


world_point_homogeneous_t1 = np.dot(homography_matrix, pixel_point_homogeneous_t1)
world_point_homogeneous_t2 = np.dot(homography_matrix, pixel_point_homogeneous_t2)

world_point_homogeneous_b1 = np.dot(homography_matrix, pixel_point_homogeneous_b1)
world_point_homogeneous_b2 = np.dot(homography_matrix, pixel_point_homogeneous_b2)

# Normalize to get the world coordinates
world_point_t1 = world_point_homogeneous_t1 / world_point_homogeneous_t1[2]
world_point_t2 = world_point_homogeneous_t2 / world_point_homogeneous_t2[2]

world_point_b1 = world_point_homogeneous_b1 / world_point_homogeneous_b1[2]
world_point_b2 = world_point_homogeneous_b2 / world_point_homogeneous_b2[2]

real_widtht=math.sqrt((world_point_t1[0][0]-world_point_t2[0][0])**2+(world_point_t1[1][0]-world_point_t2[1][0])**2)
real_widthb=math.sqrt((world_point_b1[0][0]-world_point_b2[0][0])**2+(world_point_b1[1][0]-world_point_b2[1][0])**2)

real_width=(real_widtht+real_widthb)/2

text = f"this object width in real world is {real_width}"
cv2.putText(green_copy, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)   
cv2.imshow('Image', green_copy)            
            
cv2.waitKey(0)
cv2.destroyAllWindows()