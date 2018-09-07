import cv2
import numpy as np
import matplotlib.pyplot as plt


img_l = cv2.imread('data/aloes/aloeL.jpg', 0)
img_r = cv2.imread('data/aloes/aloeR.jpg', 0)
ref = cv2.imread('data/aloes/result.png', 0)


plt.figure(1)
stereo_BM = cv2.StereoBM_create(numDisparities=144, blockSize=21) #block matching
disparity_BM = stereo_BM.compute(img_l, img_r)
plt.imshow(disparity_BM, 'gray')

plt.figure(2)
stereo_SGBM = cv2.StereoSGBM_create(numDisparities=160, blockSize=25) #block matching
disparity_SGBM = stereo_SGBM.compute(img_l, img_r)
plt.imshow(disparity_SGBM, 'gray')
plt.show()

