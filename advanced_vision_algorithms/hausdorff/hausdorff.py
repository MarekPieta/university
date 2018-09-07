import cv2 as cv2
import os
import numpy as np

def separate_contour_coords(contour):
    x = contour[:, 0, 0]
    y = contour[:, 0, 1]
    return x, y


def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)


def hausdorff_distance(x1, y1, x2, y2):
    c1 = zip(x1, y1)
    c2 = zip(x2, y2)

    dh_plus = 0
    for p1 in c1:
        min_dist = float("inf")
        for p2 in c2:
            if euclidean_distance(p1, p2) < min_dist:
                min_dist = euclidean_distance(p1, p2)
        if min_dist > dh_plus and min_dist != float("inf"):
            dh_plus = min_dist

    dh_minus = 0
    for p1 in c2:
        min_dist = float("inf")
        for p2 in c1:
            if euclidean_distance(p1, p2) < min_dist:
                min_dist = euclidean_distance(p1, p2)
        if min_dist > dh_minus and min_dist != float("inf"):
            dh_minus = min_dist
    return max(dh_minus, dh_plus)


def normalise_contour(contour):

    x, y = separate_contour_coords(contour)

    moments = cv2.moments(contour)
    x_c = moments['m10'] / moments['m00']
    y_c = moments['m01'] / moments['m00']

    width = 0
    for x1 in x:
        for x2 in x:
            if abs(x1 - x2) > width:
                width = abs(x1 - x2)

    height = 0
    for y1 in y:
        for y2 in y:
            if abs(y1 - y2) > height:
                height = abs(y1 - y2)

    x = (x - x_c) / max(width, height)
    y = (y - y_c) / max(width, height)

    return x, y