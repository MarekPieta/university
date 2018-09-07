import cv2 as cv2
import os
import numpy as np
from hausdorff import *


path = 'data/imgs/c_siros.bmp'
img = cv2.imread(path, 0)
img ^= 255
cv2.imshow('img', img)

im, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

img_color = cv2.imread(path)

cv2.drawContours(img_color, contours, -1, (0, 255, 0), 3)
cv2.imshow('img_color', img_color)

x, y = normalise_contour(contours[0])
images = os.listdir('data/imgs')

results = []
for filename in images:
    img2 = cv2.imread('data/imgs/' + filename, 0)
    img2 ^= 255
    im2, contours2, hierarchy2 = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x2, y2 = normalise_contour(contours2[0])
    hausdorff = hausdorff_distance(x, y, x2, y2)
    results.append([filename, hausdorff])
results = np.array(results)
print(results[np.argmin(results, axis=0)[1], :])

cv2.waitKey(0)