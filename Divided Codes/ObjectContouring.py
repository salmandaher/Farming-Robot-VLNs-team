import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _,img = cap.read() #cv2.imread('C:/Users/lightdsy/Desktop/mws/pythoon/image_for_cali/ghadeer.jpg')
    #img = cv2.resize(img, None, fx= 0.5, fy= 0.5, interpolation= cv2.INTER_LINEAR)
    img = cv2.resize(img, (700,500), interpolation= cv2.INTER_LINEAR)

    green_copy = img.copy()
    hsv_image = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lowgreen = np.array([83,31,42])
    highgreen = np.array([110,131,206])

    green_mask=cv2.inRange(hsv_image,lowgreen,highgreen)


    green_contours, hierarchy = cv2.findContours(image=green_mask, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)

    contours_g = sorted(green_contours, key=cv2.contourArea, reverse=True)[:1]
    cx,cy=0,0
    sized=0
    for contour in contours_g:
        cx1,cy1=0,0
        if cv2.contourArea(contour)>0:
            sized=1
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx1 = int(M["m10"] / M["m00"])
            cy1 = int(M["m01"] / M["m00"])
        bottom_most_point = tuple(contour[contour[:, :, 1].argmax()][0])
        cx2,cy2=bottom_most_point[0],bottom_most_point[1]
        cx=int((cx1+cx2)/2)
        cy=int((cy1+cy2)/2)
    cv2.drawContours(img, [contours_g], -1, (0, 255, 0), 2)
    cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)
    
    
    cv2.imshow('Video', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break