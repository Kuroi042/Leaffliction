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
        self.tresh = None
        self.blur =  None
        self.mask =  None
        self.roi =None
        self.mask1 = None
 
        pcv.params.debug = self.debug
        pcv.params.debug_outdir = self.outdir

    
    def read_orginal(self):  
        self.rgb,_,_=pcv.readimage(filename=self.path, mode="native")
        if self.rgb is not None:
            print("rgb is here successfully ! ")
        self.rgb =cv2.cvtColor(self.rgb , cv2.COLOR_BGR2RGB)
        return self.rgb
        
    def gaussian_blur(self):
        if self.rgb is None:
            self.read_orginal()
        gray = pcv.rgb2gray_hsv(rgb_img=self.rgb, channel="s")
        # plt.imshow(gray)
        blur = cv2.GaussianBlur(gray, (7, 7), 1)

        thresh = pcv.threshold.binary(
        gray_img=blur,
        threshold=65,
        object_type="light"
        )
        self.blur = thresh

        print("blur is here")
        return self.blur

    def mask_filter(self):
        if self.blur is None:
            self.gaussian_blur()
        thresh_blur = pcv.threshold.binary(
            gray_img=self.blur,
            threshold=127,
            object_type="light"
        )
        self.mask1 = pcv.fill(
            bin_img=thresh_blur,
            size=200
        )
 
        self.mask = pcv.apply_mask(
        img=self.rgb,
        mask=self.mask1,
        mask_color="white")
        plt.imshow(self.mask)
        plt.show()
        return self.mask
    def Roi(self):

        roi =  pcv.roi.rectangle(img=self.rgb, x=0,y=0,
                                w = self.rgb.shape[1],
                                h=self.rgb.shape[1])
        # *cleaned mask with only leaf pixels
        filtered_mask = pcv.roi.filter(
            mask=self.mask1,# * black and white img
            roi=roi, # * defined rect
            roi_type="partial"
        )
        # * green where leaf is, black where background is
        colored = pcv.visualize.colorize_masks(
            masks=[filtered_mask],
            colors=["green"]
        )
        # * image ready for matplotlib display
        original_rgb = cv2.cvtColor(
        self.rgb,cv2.COLOR_BGR2RGB)

        # * original + green  blended 2gether
        blended = cv2.addWeighted(
        original_rgb, 0.5,colored, 0.6,0)
        contours, _ = cv2.findContours(
        filtered_mask, ## *  black/white mask to find edges in
        cv2.RETR_EXTERNAL, ## outer cadre
        cv2.CHAIN_APPROX_NONE ##)
        )
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(
        blended,
        (x, y),
        (x + w, y + h),
        (0, 0, 255),
        3
    )
        self.roi = blended
        # plt.imshow(self.roi)
        # plt.show()
        return self.roi


    def display(self):
        if self.rgb is None:
            self.read_orginal()
        if self.blur is None:
            self.gaussian_blur()
        if self.mask is None:
            self.mask_filter()

        fig, axes = plt.subplots(1, 4, figsize=(15, 5))
        axes[0].imshow(self.rgb)
        axes[0].set_title("Figure IV.1 : Original")
        axes[0].axis("off")

        axes[1].imshow(self.blur, cmap="gray")
        axes[1].set_title("Figure IV.2 : Blur/Threshold")
        axes[1].axis("off")

        axes[2].imshow(self.mask)
        axes[2].set_title("Figure IV.3 :Masked")
        axes[2].axis("off")
        axes[3].imshow(self.roi)
        axes[3].set_title("Figure IV.3 :Masked")
        axes[3].axis("off")

        plt.tight_layout()
        plt.show()
    
def Execute_filter(tools:handytools):
    leaf  =  Transforme(tools)
    leaf.read_orginal()
    leaf.gaussian_blur()
    leaf.mask_filter()
    leaf.Roi()
    leaf.display()


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

    

    
