import matplotlib.pyplot as plt
import os ,sys
import pandas as pd
import numpy as np
from plantcv import plantcv as pcv
from pathlib import Path
import cv2
class handytools:
    def __init__(self, path,debug=None, outdir="."):
        self.image = path
        self.debug = debug
        self.outdir = outdir
        if not os.path.isdir(self.outdir):
            os.makedirs(self.outdir)

class Transforme:
    def __init__(self, tools:handytools):
        self.path = tools.image
        self.debug =  tools.debug
        self.outdir = tools.outdir
        self.rgb =   None
        # self.tresh = None
        self.blur =  None
        self.mask =  None
        pcv.params.debug = self.debug
        pcv.params.debug_outdir = self.outdir

    
    def read_orginal(self):  
        self.rgb,_,_=pcv.readimage(filename=self.path, mode="native")
        if self.rgb is not None:
            print("rgb is here successfully ! ")
        plt.imshow(self.rgb)
        plt.show()
        
        return self.rgb
    def gaussian_blur(self):
        if self.rgb is None:
            self.read_orginal()
        gray = pcv.rgb2gray_hsv(rgb_img=self.rgb, channel="s")
        thresh = pcv.threshold.binary(gray_img=gray,
                 threshold=60,  object_type="light")
        self.blur = pcv.gaussian_blur(
            img=thresh,
            ksize=(5, 5),
            sigma_x=0,
            sigma_y=None
        )

    #     _, self.blur = cv2.threshold(
    #     blurred,
    #     0,
    #     255,
    #     cv2.THRESH_BINARY + cv2.THRESH_OTSU
    # )
        print("blur is here")
        plt.imshow(self.blur,cmap="gray")
        plt.show()
        return self.blur
    
    def mask_filter(self):
        if self.blur is None:
            self.gaussian_blur()
        thresh_blur = pcv.threshold.binary(
            gray_img=self.blur,
            threshold=127,
            object_type="light"
        )

        mask1 = pcv.fill(
            bin_img=thresh_blur,
            size=200
        )
        self.mask = pcv.apply_mask(
        img=self.rgb,
        mask=mask1,
        mask_color="white"
    )
        plt.imshow(self.mask)
        plt.show()
        return self.mask
    
def Execute_filter(tools:handytools):
    leaf  =  Transforme(tools)
    leaf.read_orginal()
    leaf.gaussian_blur()
    leaf.mask_filter()


def main():
    try:
        assert len(sys.argv) == 2 , "argument are bad"
    except AssertionError as e:
        print(f"AssertionError:{e}")
        sys.exit(1)
    path = Path(str(sys.argv[1]))
    tools = handytools(path, None,outdir="./tmp")
    Execute_filter(tools)
    # read_orginal()
if __name__ == "__main__":
    main()

    

    
