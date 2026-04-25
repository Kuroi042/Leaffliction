import matplotlib.pyplot as plt
import os ,sys
import pandas as pd
import numpy as np
from plantcv import plantcv as pcv
from pathlib import Path
import cv2

def    Execute_filter(Path):
    import matplotlib
    # pcv.params.debug = "plot" 
    img, _, _ = pcv.readimage(filename=Path, mode="native")
    
    # colors = pcv.visualize.colorspaces(rgb_img=img, original_img=False)
    # plt.imshow(colors, cmap='gray')
    # a = pcv.rgb2gray_lab(img, 'a')
    # blur = pcv.gaussian_blur(img=a, ksize=(5,5))
    # # bin_gauss1 = pcv.threshold.gaussian(gray_img=blur, ksize=31, offset=7,object_type='dark')
    # thresh = pcv.threshold.otsu(
    # gray_img=blur,
    # object_type='dark'
# )
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(hsv,(5,5),0)
    plt.imshow(blur, cmap='gray')

    plt.show()
def main():
    try:
        assert len(sys.argv) == 2 , "argument are bad"
    except AssertionError as e:
        print(f"AssertionError:{e}")
        sys.exit(1)
    path = Path(str(sys.argv[1]))
    Execute_filter(path)
if __name__ == "__main__":
    main()
