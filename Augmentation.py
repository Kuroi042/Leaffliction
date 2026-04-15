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

def operate(path:str):

    img  = cv2.imread(path)
    cv2.imshow('img',img)
    ft_rotate(path)
    ft_flip(path)
    


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
        