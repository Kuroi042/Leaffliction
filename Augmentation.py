import cv2
import os
import sys
import numpy as np
import random as rnd
from pathlib import Path
cv2.namedWindow('img', cv2.WINDOW_NORMAL)

def operate(path:str):

    img  = cv2.imread(path)
    #range 15-20 degrees
    # img_flip =  cv2.flip(img,rnd.randrange(-1,1)) # range between -1->1
    # cv2.imshow('imgflip',img_flip)
    img_rotate =  cv2.rotate(img)
    
    cv2.imshow('img',img)
    cv2.waitKey(0)
    


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
        