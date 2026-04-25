import cv2
import os

img = cv2.imread(os.path.join('Apple/Apple_Black_rot/image (1).JPG'))
hsv =  cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h =  hsv[:,:,0]
s = hsv[:,:,1]
v =hsv[:,:,2]


cv2.imshow("original" , img)
cv2.imshow("hue" , h)
cv2.imshow("saturation" , s)
cv2.imshow("value" , v)

cv2.waitKey(0)

