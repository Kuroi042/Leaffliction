import matplotlib.pyplot as plt
import os ,sys
import pandas as pd
import numpy as np
from plantcv import plantcv as pcv
from pathlib import Path
import cv2

def    Execute_filter(Path):
    import matplotlib
    img, _, _ = pcv.readimage(filename=Path, mode="native")
    gray = pcv.rgb2gray_hsv(rgb_img=img, channel="s")    
    thresh = pcv.threshold.binary(
            gray_img=gray, threshold=60,  object_type="light"
        )
    blur = pcv.gaussian_blur(img=thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)
    # mask = pcv.fill(blur, size=200)
    blur_thresh = pcv.threshold.binary(
        gray_img=blur,
        threshold=127,
        object_type="light"
    )
    mask = pcv.fill(
        bin_img=blur_thresh,
        size=200
    )
    masked = pcv.apply_mask(
        img=img,
        mask=mask,
        mask_color="white"
    )

    plt.imshow(blur_thresh)
    # plt.imshow( masked)
    plt.show()
    plt.show()
    # return blur
    #### mask

# def mask(path:str):

    

    

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
