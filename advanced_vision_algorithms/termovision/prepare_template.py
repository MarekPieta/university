import cv2
import numpy as np
import os


images = os.listdir('chosen_templates')

DPM = np.zeros((192, 64))

results = []
for filename in images:
    img = cv2.imread('chosen_templates/' + filename, 0)
    img = cv2.resize(img, (64, 192), interpolation=cv2.INTER_CUBIC)
    _, img_binary = cv2.threshold(img, 40, 1, cv2.THRESH_BINARY)
    DPM += img_binary
    cv2.imshow('temp', img)

cv2.imwrite('probabilistic.png', DPM)