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
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # step 2: apply gaussian blur
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(
        blur,
        0,      # threshold value
        255,    # max value
        cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU
    )

    plt.imshow( thresh, cmap='gray')
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
