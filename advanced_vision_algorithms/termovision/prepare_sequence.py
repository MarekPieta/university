import cv2
import numpy as np

cap = cv2.VideoCapture('data/vid1_IR.avi')

i = 0
while cap.isOpened():
    ret, frame = cap.read()
    if frame is None:
        break
    cv2.imwrite('data/sequence/frame_%06d.png' % i, frame)
    i += 1
