import matplotlib.pyplot as plt
import os ,sys
import pandas as pd
import numpy as np
from plantcv import plantcv as pcv
from pathlib import Path
import cv2

def    Execute_filter(Path):
    pcv.params.debug = None
    img, _, _ = pcv.readimage(filename=Path, mode="native")
    gray = pcv.rgb2gray(rgb_img=img)
    threshold_dark = pcv.threshold.otsu(gray_img=gray, object_type='dark')

    cv2.imshow("Image", threshold_dark)
    cv2.waitKey(0)
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
