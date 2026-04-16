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
# def ft_contrast(path:str):
#     img  =  cv2.imread(path)
#     alpha =  np.random.uniform(1.1, 2.5)
#     beta =  np.random.randint(-20, 20)
#     img_contrast = cv2.convertScaleAbs(img , alpha=alpha, beta= beta)
#     cv2.imshow('img_contrast', img_contrast)
#     cv2.waitKey(0)
def ft_flip(path:str):
    img  =  cv2.imread(path)
    img_flip =  cv2.flip(img,rnd.randrange(-1,1)) # range between -1->1
    cv2.imshow('imgflip',img_flip)
    cv2.waitKey(0)
# def ft_blur(path:str):
#     img =  cv2.imread(path)
#     img_blur =  cv2.blur(img,(5,5))
#     cv2.imshow('img_blur' , img_blur)
#     cv2.waitKey(0)
def ft_scaling(path:str):
    img =  cv2.imread(path)
    resized_img = cv2.resize(img, ((224, 224)))
    cv2.imshow('img_scale',resized_img)
    cv2.waitKey(0)
# def skew(path:str):

def ft_shear(path:str):
    img = cv2.imread(path)
    print(img.shape)
    h,w = img.shape[:2]
    shear_factor = 0.5
    # flipped = cv2.flip(img, 0)

    M = np.float32([[1, shear_factor, 0],
                    [0, 1, 0]])
    # [1, k, 0] = x₁ = 1*x + k*y + 0 | x1 =x
    # [0, 1, 0] =  y₁ = 0*x + 1*y + 0  | y1 =y
    
    # (x, y) = (10, 0) |  k = 0.5
    # x1 = 1 * 10 + 0.5*0 + 0 = 10.5
    # y1 = 0 + 1*0.5 +0  = 0.5
    new_w = int(w + h * shear_factor) 
    shear = cv2.warpAffine(img, M, (new_w, h))
    # result = cv2.flip(shear, 0)

    cv2.imshow('shear',shear)
    cv2.waitKey(0)
def operate(path:str):

    img  = cv2.imread(path)
    cv2.imshow('img',img)
    # ft_rotate(path)
    # ft_flip(path)
    ft_shear(path)
    # ft_blur(path)
    # ft_contrast(path)
    # ft_scaling(path)
    

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
        