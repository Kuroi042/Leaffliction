import cv2
import os
import sys
import numpy as np
import random as rnd
from pathlib import Path
cv2.namedWindow('img', cv2.WINDOW_NORMAL)

def ft_rotate(path:str):
    img  =  cv2.imread(path)
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    angle = 18 
    scale = 1.0
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated_image = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    cv2.imshow('Rotated Leaf', rotated_image)    
    cv2.waitKey(0)
def ft_flip(path:str):
    img  =  cv2.imread(path)
    img_flip =  cv2.flip(img,rnd.randrange(-1,1)) # range between -1->1
    cv2.imshow('imgflip',img_flip)
    cv2.waitKey(0)

def skew(path:str):
    image = cv2.imread(path)

    h, w = image.shape[:2]
    # how mucht he image will be skewed 10-20 of the width
    offset = rnd.randint(int(w*0.1),int(w*0.2)) #(10%-20%) of width 
    # (256, 256, 3)
    print(image.shape)
    # original 4 corners
    pts1 = np.float32([
        [0, 0],
        [w, 0],
        [0, h],
        [w, h]
    ])

    # new 4 corners → top shifted right
    # tells OpenCV where to move the pixels
    pts2 = np.float32([
        [offset, 0],
        [w + offset, 0],
        [0, h],
        [w, h]
    ])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    # add the ofset on the canvas to show the skew 
    # try h+ofset for hieght 
    result = cv2.warpPerspective(image, M, (w+offset, h))
    # print(result.shape)
    # (256, 296, 3)
    cv2.imshow('Skewed', result)
    cv2.waitKey(0)




def ft_scaling(path:str):
    img =  cv2.imread(path)
    resized_img = cv2.resize(img, ((224, 224)))
    cv2.imshow('img_scale',resized_img)
    cv2.waitKey(0)

def ft_shear(path:str):
    img = cv2.imread(path)
    print(img.shape)
    h,w = img.shape[:2]
    shear_factor = 0.3
    Mh = np.float32([[1, shear_factor, 0],
                    [0, 1, 0]])
    Mv = np.float32([[1, 0, 0],
                    [0.3 ,1, 0]])
    shear = cv2.warpAffine(img,rnd.choice([Mv, Mh]) , (w, h))
    cv2.imshow('shear',shear)
    cv2.waitKey(0)
def operate(path:str):

    img  = cv2.imread(path)
    cv2.imshow('img',img)
    # ft_rotate(path)
    # ft_flip(path)
    # ft_shear(path)
    # ft_blur(path)
    # ft_contrast(path)
    # ft_scaling(path)
    # ft_distort(path)
    skew(path)
def main():
    try:
        assert len(sys.argv) == 2 , "argument are bad"
    except AssertionError as e:
        print(f"AssertionError:{e}")
        sys.exit(1)
    path = Path(str(sys.argv[1]))
    operate(path)
if __name__ == "__main__":
    main()
        