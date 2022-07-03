# ahnjw, 2021.07.11

import cv2
import numpy as np
import glob

fps = 15
 
img_array = []
set = "set59"
for filename in sorted(glob.glob(f"/home/cym/Work/mAP/output_images_set22-82/{set}_*.jpg")):
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    print(size)
    img_array.append(img)
 
#out = cv2.VideoWriter(f"{set}.mp4", cv2.VideoWriter_fourcc(*'DIVX'), 10, size)
out = cv2.VideoWriter(f"{set}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])

out.release()

print(f"\nCreating {set}.mp4 succeeded..") 
