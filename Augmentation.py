import cv2
import os
import sys
import numpy as np
import random as rnd
from pathlib import Path
import matplotlib.pyplot as plt




def Name_Maker(path:str , func:str):
    path2 =  Path(*path.parts[:2])
    name  =  str(path).split("/")[2]    
    slimame = name.split('.')[0]
    ext =  name.split('.')[1]
    # print(slimame,ext)
    # print(slimame ,'+' ,ext)
    save_path =  os.path.join(path2, slimame+func+'.'+ext)
    print(f"Saving {func} Done !!!")

    return save_path


def ft_rotate(path:str):
    img  =  cv2.imread(path)
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    angle = 18 
    scale = 1.0
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated_image = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    save_path = Name_Maker(path,'_Rotate')
    print(save_path)
    cv2.imwrite(save_path, rotated_image)
    return rotated_image

def ft_flip(path:str):
    img  =  cv2.imread(path)
    img_flip =  cv2.flip(img,rnd.choice([-1,0,1])) # range between -1->1
    save_path = Name_Maker(path,'_Flip')
    cv2.imwrite(save_path, img_flip)
    return img_flip

def skew(path:str):
    image = cv2.imread(path)

    h, w = image.shape[:2]
    # how mucht he image will be skewed 10-20 of the width
    offset = rnd.randint(int(w*0.1),int(w*0.2)) #(10%-20%) of width 
    # (256, 256, 3)
    # original 4 corners
    pts1 = np.float32([
        [0, 0],
        [w, 0],
        [0, h],
        [w, h]
    ])

    # new 4 corners → top shifted right
    # tells OpenCV where to move the pixels
    pts2 = np.float32([
        [offset, 0],
        [w + offset, 0],
        [0, h],
        [w, h]
    ])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    # add the ofset on the canvas to show the skew 
    # try h+ofset for hieght 
    result = cv2.warpPerspective(image, M, (w+offset, h),borderMode=cv2.BORDER_REFLECT)
    # print(result.shape)
    # (256, 296, 3)
    save_path = Name_Maker(path,'_Skew')
    cv2.imwrite(save_path, result)
    return result


def ft_crop(path:str):
    img  = cv2.imread(path)
    h, w =  img.shape[:2]
    ratio = rnd.choice([0.7,0.8,0.9])
    new_h =  h*ratio
    new_w =  w*ratio
    starty= int((h - new_h)//2) 
    end_y = int(starty + new_h) 
    startx = int((w-new_w)//2)
    endx =  int(startx +  new_w)
    result=  img[starty:end_y, startx:endx]
    save_path = Name_Maker(path,'_Crop')
    cv2.imwrite(save_path, result)
    return result
    

def ft_scaling(path:str):
    img =  cv2.imread(path)
    resized_img = cv2.resize(img, ((224, 224)))
    save_path = Name_Maker(path,'_Scale')
    cv2.imwrite(save_path, resized_img)
    return resized_img


def ft_shear(path:str):
    img = cv2.imread(path)
    h,w = img.shape[:2]
    shear_factor = rnd.uniform(0.2, 0.4)
    Mh = np.float32([[1, shear_factor, 0],
                    [0, 1, 0]])
    Mv = np.float32([[1, 0, 0],
                    [0.3 ,1, 0]])
## for black border same for skew and shear     
    shear = cv2.warpAffine(img,rnd.choice([Mv, Mh]) , (w, h),borderMode=cv2.BORDER_REFLECT) 
    save_path = Name_Maker(path,'_Shear')
    cv2.imwrite(save_path, shear)
    return shear



def distort(path:str):
    # print(path)
    name =  str(path).split('/')[2]
    # print(name)
    img = cv2.imread(path)
    h, w = img.shape[:2]

    strength = rnd.randrange(50,80)

    map_x, map_y = np.meshgrid(
        np.arange(w),
        np.arange(h)
    )

    # force float32 from the start
    map_x = map_x.astype(np.float32)
    map_y = map_y.astype(np.float32)

    noise_x = (np.random.randn(h, w) * strength).astype(np.float32)
    noise_y = (np.random.randn(h, w) * strength).astype(np.float32)

    # blur the noise
    noise_x = cv2.GaussianBlur(noise_x, (51, 51), 0).astype(np.float32)
    noise_y = cv2.GaussianBlur(noise_y, (51, 51), 0).astype(np.float32)

    # add noise to maps
    map_x = map_x + noise_x
    map_y = map_y + noise_y

    # final safety cast
    map_x = map_x.astype(np.float32)
    map_y = map_y.astype(np.float32)

    distorted = cv2.remap(
        img,
        map_x,
        map_y,
        cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )
    # path =  str(path).split('/')[[0],[1]]
    save_path = Name_Maker(path,'_Distortion')
    
    cv2.imwrite(save_path, distorted)
    return distorted

def display(path: str, results: dict):
    names = list(results.keys())
    images = list(results.values())

    # 4 rows: original + 3 pairs
    fig, axes = plt.subplots(4, 2, figsize=(10, 16))
    axes = axes.flatten()

    for i in range(7):
        img_rgb = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
        axes[i].imshow(img_rgb)
        axes[i].set_title(names[i], fontsize=12)
        axes[i].axis('off')

    # hide the last empty subplot
        axes[7].axis('off')

    plt.suptitle('Augmentations', fontsize=16)
    plt.tight_layout()
    plt.show()

def operate(path:str):
    original =  cv2.imread(str(path))

    results = {
        'Original' :original,
        'Rotate': ft_rotate(path),
        'Flip': ft_flip(path),
        'Shear': ft_shear(path),
        'Skew': skew(path),
        'Crop': ft_crop(path),
        'Distortion': distort(path)
    }
    display(path, results)

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
        