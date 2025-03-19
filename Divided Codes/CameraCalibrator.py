import numpy as np
import cv2
import glob

# Define the criteria for corner refinement
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points for a 10x7 chessboard
objp = np.zeros((7*10, 3), np.float32)
objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2)

# Arrays to store object points and image points from all images
objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

# Read images from a directory
images = glob.glob('C:/Users/lightdsy/Desktop/WRO/mws/*.jpg')

# Initialize gray variable
cnt=0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (10, 7), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
       cnt+=1
       objpoints.append(objp)
       corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
       imgpoints.append(corners2)
       #Draw and display the corners
    #    img = cv2.drawChessboardCorners(img, (10, 7), corners2, ret)
    #    cv2.imshow('img', img)
    #    cv2.waitKey(500)
    else: 
       print("pattern not found")

cv2.destroyAllWindows()

# Check if any images were processed
if gray is not None:
    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Save the camera calibration results
    #np.savez('calibration.npz', ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    # Print the camera calibration results
    print("Camera matrix:\n", mtx)
    print("Distortion coefficients:\n", dist)
    print("Rotation vectors:\n", rvecs)
    print("Translation vectors:\n", tvecs)
    
    for i in range(len(rvecs)):
        # Convert rotation vector to rotation matrix
        R, _ = cv2.Rodrigues(rvecs[i])

        # Get the translation vector
        t = tvecs[i]

        # Construct the extrinsic matrix [R | t]
        extrinsic_matrix = np.hstack((R, t))

        print(f"Extrinsic matrix for image {i+1}:\n", extrinsic_matrix)
else:
    print("No images were processed. Ensure that the image path is correct and images are accessible.")

print(cnt)
