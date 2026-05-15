import cv2
import os
import plantcv as pcv
img = cv2.imread(os.path.join('Apple/Apple_Black_rot/image (1).JPG'))
blur =  cv2.blur(img, ksize=(7,7) )
cv2.imshow("sdasd",blur)
cv2.waitKey(0)
