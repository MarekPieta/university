import cv2
import numpy as np
import os


def find_template(img, DPM_0, DPM_1):
    result = np.zeros((img.shape[0] - DPM_1.shape[0], img.shape[0] - DPM_1.shape[1]), np.float32)


    for y in range(0, result.shape[0]):
        for x in range(0, result.shape[1]):
            fragment = img[y:(y + DPM_1.shape[0]), x:(x + DPM_1.shape[1])]
            correlation = DPM_1 * fragment
            correlation += (1 - DPM_0) * fragment
            result[y, x] = sum(sum(correlation))

    result = result / np.max(np.max(result))
    ruint8 = np.uint8(result * 255)
    return ruint8


cap = cv2.VideoCapture('data/vid1_IR.avi')
number_of_template_images = 35
template = cv2.imread('probabilistic.png', 0)
DPM_1 = np.float32(template)

DPM_1 = DPM_1 / number_of_template_images
DPM_0 = 1 - DPM_1

frame = cv2.imread('data/sequence/frame_000450.png', 0)
_, frame_binary = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY)

frame_color = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

thresh = 230
location_thresh_1 = 100
location_thresh_2 = 70
maxima = []

res = find_template(frame_binary, DPM_1, DPM_0)
maximum = (np.argmax(res) / len(res[0]), np.argmax(res) % len(res[0]))
cv2.rectangle(frame_color, (int(maximum[1]), int(maximum[0])),
          (int(maximum[1]) + DPM_1.shape[1], int(maximum[0]) + DPM_1.shape[0]), (0, 255, 0))
maxima.append(maximum)
res[int(maximum[0])][int(maximum[1])] = 0

while np.max(res) > thresh:
    maximum = (np.argmax(res)/len(res[0]), np.argmax(res)%len(res[0]))
    isClose = False
    for j in maxima:
        if ((j[0] - maximum[0])**2 < location_thresh_1 or (j[1] - maximum[1])**2) < location_thresh_2:
            isClose = True
    if not isClose:
        maxima.append(maximum)
        cv2.rectangle(frame_color, (int(maximum[1]), int(maximum[0])),
          (int(maximum[1]) + DPM_1.shape[1], int(maximum[0]) + DPM_1.shape[0]), (0, 255, 0))
    res[int(maximum[0])][int(maximum[1])] = 0
#print(np.max(res))
cv2.imshow('frame', frame_color)
cv2.waitKey(0)

