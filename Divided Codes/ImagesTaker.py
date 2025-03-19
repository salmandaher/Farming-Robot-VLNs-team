import cv2

# Start video capture from the default camera (usually the laptop's webcam)
# "USB/VID_046D&PID_082D&MI_00/6&141BD825&0&0000"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

frame_count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (700,500), interpolation= cv2.INTER_LINEAR) #third arg is fucking optinal and you could put the tuble in the second arg directly (300,200)


    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Wait for a key press for 1ms
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        # Save the current frame
        frame_filename = f'frame_{frame_count:04d}.jpg'
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")
        frame_count += 1

    elif key == ord('q'):
        # Exit the loop
        print("Exiting...")
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
