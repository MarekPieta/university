import cv2 as cv2
import os
import numpy as np
from hausdorff import *


whole_map = cv2.imread('data/Aegeansea.jpg')
whole_map = cv2.cvtColor(whole_map, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(whole_map)

thresh1, s = cv2.threshold(s, 30, 255, cv2.THRESH_BINARY)
thresh2, h = cv2.threshold(h, 60, 255, cv2.THRESH_BINARY_INV)
whole_map_binary = s & h

#kernel = np.ones((3,3),np.uint8)

#whole_map_binary = cv2.dilate(whole_map_binary, kernel)
#whole_map_binary = cv2.erode(whole_map_binary, kernel)


whole_map_with_contours, contours, hierarchy = cv2.findContours(whole_map_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

contours = list(filter(lambda el : el.shape[0]>15 and el.shape[0]<3000, contours))

images_titles = os.listdir('data/imgs')
whole_map_color = cv2.cvtColor(whole_map_binary, cv2.COLOR_GRAY2BGR)

for i in images_titles:
    img_test = cv2.imread( 'data/imgs/'+ i, 0)
    # t_limnos,

    img_test ^= 255
    img_test, contours_test, hierarchy_test = cv2.findContours(img_test, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y = normalise_contour(contours_test[0])

    hausdorffs = []

    for c in range(0, len(contours)):
        x2, y2 = normalise_contour(contours[c])
        hausdorff = hausdorff_distance(x, y, x2, y2)
        hausdorffs.append(hausdorff)

    hausdorffs = np.array(hausdorffs)
    found_index = np.argmin(hausdorffs, axis=0)

    moments = cv2.moments(contours[found_index], 1)
    x_c = moments['m10'] / moments['m00']
    y_c = moments['m01'] / moments['m00']


    cv2.putText(whole_map_color, i.split('_')[1].split('.')[0], (int(x_c), int(y_c)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0))
    #cv2.drawContours(whole_map_color, contours[found_index], -1, (0, 255, 0), 3)



cv2.namedWindow('Whole map', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Whole map', 800, 800)
cv2.imshow('Whole map', whole_map_color)



cv2.waitKey(0)