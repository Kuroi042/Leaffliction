import matplotlib.pyplot as plt
import os ,sys
import pandas as pd
import numpy as np
from plantcv import plantcv as pcv
from pathlib import Path
import cv2
import math

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
        self.max_thresh = None
        self.blur =  None
        self.mask =  None
        self.filtered_mask =None

        self.roi =None
        self.mask1 = None
        self.analyzed =  None
 
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
        threshold=65, ## * low 
        object_type="light"
        )
        self.blur = thresh

        print("blur is here")
        return self.blur

    def mask_filter(self):
        if self.blur is None:
            self.gaussian_blur()
        # thresh_blur = pcv.threshold.binary(
        #     gray_img=self.blur,
        #     threshold=127,
        #     object_type="light"
        # )
        self.mask1 = pcv.fill(
            bin_img=self.blur,
            size=200
        )
 
        self.mask = pcv.apply_mask(
        img=self.rgb,
        mask=self.mask1,
        mask_color="white")
        # plt.imshow(self.mask)
        # plt.show()
        return self.mask
    '''
    1- rectangle covers the entire image
    2- cleaned mask with only leaf pixels
    3- green where leaf is, black where background is
    4- image ready for matplotlib display
    5- original + green overlay blended together
    6- list of contours (leaf edges)
    7- _largest_  the leaf contour (biggest object)
    8- 4 numbers defining rectangle around leaf
    9- blue rectangle drawn around the leaf
    '''

    def Roi(self):

        roi =  pcv.roi.rectangle(img=self.rgb, x=0,y=0,
                                w = self.rgb.shape[1],
                                h=self.rgb.shape[1])
        # *cleaned mask with only leaf pixels
        self.filtered_mask = pcv.roi.filter(
            mask=self.mask1,# * black and white img
            roi=roi, # * defined rect
            roi_type="partial"
        )
        # * green where leaf is, black where background is
        colored = pcv.visualize.colorize_masks(
            masks=[self.filtered_mask],
            colors=["green"]
        )
        # * image ready for matplotlib display
        original_rgb = cv2.cvtColor(
        self.rgb,cv2.COLOR_BGR2RGB)

        # * original + green  blended 2gether
        blended = cv2.addWeighted(
        original_rgb, 0.5,colored, 0.6,0)
        contours, _ = cv2.findContours(
        self.filtered_mask, ## *  black/white mask to find edges in
        cv2.RETR_EXTERNAL, ## outer cadre
        cv2.CHAIN_APPROX_NONE ##)
        )
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(
        blended,
        (x, y),
        (x + w, y + h),
        (0, 0, 255), ### blue contour
        3 
    )
        self.roi = blended
        return self.roi
    

    '''
    find the leaf shape
    draw its outline in pink
    find its center point
    draw a cross at center
    draw inner details in blue
    '''

    def analyze_object(self):
        if self.roi is None:
            self.mask_filter()

        #1: copy original image
        analyze_img = self.rgb

        #2 find inner contours for the leaf using the mask 
        ###* list of contour point around leaf edge
        contours, _ = cv2.findContours(
            self.filtered_mask, ###* black and white mask 
            cv2.RETR_EXTERNAL, ####* OUTER edges only
            cv2.CHAIN_APPROX_SIMPLE ###* compress points to save memory len ~4
        )
        if not contours: ##*jad3ana
            print("no contours found!")
            return None
        #*3: get ONLY 1 largest contour "contour1"
        largest = max(contours, key=cv2.contourArea)##* contoursArea get values from findcoutours
        # step 4: draw pink outline around leaf
        cv2.drawContours( ###* perfect contoure pink 
            analyze_img,
            [largest], ##* only one cntour fron max()
            -1,
            (0, 0, 255),  # pink/magenta
            10
        )
############################################***
        # step 5: find centroid 
###* the average position of all pixels in the leaf shape
##* distance of spots from center
##* spread direction of disease
####*
#*Convex Hull
#*Smooth outer perimeter of leaf
#*Centroid    ↓
#*Center point of leaf
#*Vertical Axis
#* Line passing through centroid
#*Tip Line    ↓
#* Line from centroid to farthest point on leaf
        hull = cv2.convexHull(largest)

        # Convex Hull
        cv2.drawContours(
            analyze_img,
            [hull],
            -1,
            (255, 0, 255),
            10
        )

        # Centroid
        M = cv2.moments(largest)
        if M["m00"] != 0:

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Draw centroid
            cv2.circle(
                analyze_img,
                (cx, cy),
                10,
                (255, 0, 255),
                -1
            )
            # Vertical axis
            cv2.line(
                analyze_img,
                (cx, 0),
                (cx, analyze_img.shape[0]),
                (255, 0, 255),
                5
            )
            # Find leaf tip
            hull_pts = hull.reshape(-1, 2)

            distances = np.sqrt(
                (hull_pts[:, 0] - cx) ** 2 +
                (hull_pts[:, 1] - cy) ** 2
            )

            tip = hull_pts[np.argmax(distances)]
            tip_x = int(tip[0])
            tip_y = int(tip[1])
            
            # --- EXTEND LINE TO OPPOSITE SIDE ---
            
            # 1. Get the direction vector from centroid to tip
            dx = tip_x - cx
            dy = tip_y - cy
            
            # 2. Normalize this vector so its length is 1
            line_len = np.sqrt(dx**2 + dy**2)
            ux = dx / line_len
            uy = dy / line_len
            
            # 3. Project all hull points onto this line axis to find the opposite extreme
            # (This ensures the opposite point is perfectly aligned with the diagonal)
            hull_vectors_x = hull_pts[:, 0] - cx
            hull_vectors_y = hull_pts[:, 1] - cy
            projections = (hull_vectors_x * ux) + (hull_vectors_y * uy)
            
            # The tip is the maximum projection, the opposite side is the minimum projection
            min_projection = np.min(projections)
            
            # 4. Calculate the perfect starting point on the opposite side
            opposite_x = int(cx + min_projection * ux)
            opposite_y = int(cy + min_projection * uy)

            # Draw the FULL diagonal line passing through the centroid
            cv2.line(
                analyze_img,
                (opposite_x, opposite_y), # Starts at the opposite base/stem side
                (tip_x, tip_y),           # Ends at the tip
                (255, 0, 255),
                5
            )
####################################**        
        self.analyzed = analyze_img

        plt.imshow(self.analyzed)
        plt.title('Analyze Object')
        plt.axis('off')
        plt.show()

        return self.analyzed

    def display(self):
        if self.rgb is None:
            self.read_orginal()
        if self.blur is None:
            self.gaussian_blur()
        if self.mask is None:
            self.mask_filter()

        fig, axes = plt.subplots(1, 5, figsize=(15, 6))
        axes[0].imshow(self.rgb)
        axes[0].set_title("Figure I.1 : Original")
        axes[0].axis("off")

        axes[1].imshow(self.blur, cmap="gray")
        axes[1].set_title("Figure II.2 : Blur/Threshold")
        axes[1].axis("off")

        axes[2].imshow(self.mask)
        axes[2].set_title("Figure IV.3 :Masked")
        axes[2].axis("off")

        axes[3].imshow(self.roi)
        axes[3].set_title("Figure V.4 :Roi")
        axes[3].axis("off")

        axes[4].imshow(self.analyzed)
        axes[4].set_title("Figure VI.3 :Analysed ")
        axes[4].axis("off")

        plt.tight_layout()
        plt.show()
    
def Execute_filter(tools:handytools):
    leaf  =  Transforme(tools)
    leaf.read_orginal()
    leaf.gaussian_blur()
    leaf.mask_filter()
    leaf.Roi()
    leaf.analyze_object()
    # leaf.display()


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

    

    
