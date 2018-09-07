import cv2
import numpy as np


im = cv2.imread('data/trybik.jpg', 0)
thresh1, im_binary = cv2.threshold(im, 235, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('Gray', im)
cv2.imshow('Binary', im_binary)
im_cnt, contours, hierarchy = cv2.findContours(im_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


sobelx = cv2.Sobel(im, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(im, cv2.CV_64F, 0, 1, ksize=5)

gradient_value = (sobelx**2 + sobely**2)**0.5
gradient_value = gradient_value / np.max(gradient_value)
gradient_orientation = np.arctan2(sobely, sobelx)

moments = cv2.moments(im_binary, 1)
x_c = moments['m10'] / moments['m00']
y_c = moments['m01'] / moments['m00']


Rtable = [[] for i in range(360)]

for i in contours[0]:
    amplitude = ((i[0][0] - x_c)**2 + (i[0][1] - y_c)**2)**0.5
    phase = np.arctan2(i[0][1] - y_c, i[0][0] - x_c)
    phase = phase * 360 / (2 * np.pi) + 180
    place = int(round(gradient_orientation[i[0][0], i[0][1]] * 360 / (2*np.pi) + 180))
    if place == 360:
        place = 0
    Rtable[place].append([amplitude, phase])

im2 = cv2.imread('data/trybiki2.jpg', 0)
sobelx2 = cv2.Sobel(im2, cv2.CV_64F, 1, 0, ksize=5)
sobely2 = cv2.Sobel(im2, cv2.CV_64F, 0, 1, ksize=5)

gradient_value2 = (sobelx2**2 + sobely2**2)**0.5
gradient_value2 = gradient_value2 / np.max(gradient_value2)

gradient_orientation2 = np.arctan2(sobely2, sobelx2)


w, h = gradient_value2.shape

result = np.zeros([2*w, 2*h], np.float)
result = np.zeros(result.shape + (36,), np.float)


for x in range(0, w):
    for y in range(0, h):
        if gradient_value2[x, y] > 0.5:
            phi = int(round(gradient_orientation2[x][y] * 360 / (2 * np.pi) + 180))
            if phi == 360:
                phi = 0
            for i in Rtable[phi]:
                amplitude = i[0]
                phase = i[1]
                for j in range(0, 35):
                    x1 = int(round(amplitude * np.cos(phase * np.pi / 180) + x))
                    y1 = int(round(amplitude * np.sin(phase * np.pi / 180) + y))
                    result[y1, x1, j] += 1
                    phase -= 10
                    if phase < 0:
                        phase += 360


im2_color = cv2.imread('data/trybiki2.jpg')

found_mass_center = np.unravel_index(result.argmax(), result.shape)
delta = 30

for j in range(0, 3):
    result[found_mass_center[0]-delta:found_mass_center[0]+delta, \
    found_mass_center[1]-delta:found_mass_center[1]+delta, :] = 0
    found_mass_center = np.unravel_index(result.argmax(), result.shape)
    cv2.circle(im2_color, (found_mass_center[0], found_mass_center[1]), 1, (0, 255, 0), thickness=3)

cv2.imshow('Found', im2_color)


cv2.waitKey(0)
