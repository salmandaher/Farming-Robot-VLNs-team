import cv2

x1=0
y1=0
# Define the callback function to capture mouse events
def show_coordinates(event, x, y, flags, param):
    global x1,y1
    if event == cv2.EVENT_MOUSEMOVE:
        # Display the coordinates
        img_copy = resized.copy()
        x1=x
        y1=y
        text = f"X: {x}, Y: {y}, Color: {img[y, x]}"
        cv2.putText(img_copy, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow('Image', img_copy)

# Load an image
img = cv2.imread('C:/Users/lightdsy/Desktop/mws/pythoon/image_for_cali/fuckingjob.jpg')
resized = cv2.resize(img, (700,500), interpolation= cv2.INTER_LINEAR)

# Create a window and set a mouse callback function
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', show_coordinates)


while True:
    # Display the image
    img_copy=resized.copy()
    text = f"X: {x1}, Y: {y1}, Color: {img[y1, x1]}"
    cv2.putText(img_copy, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow('Image', img_copy)
    
    # Break the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
