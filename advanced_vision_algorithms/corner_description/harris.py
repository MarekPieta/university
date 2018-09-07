import cv2
import numpy as np
import matplotlib.pyplot as plt


def localMaxima(I, min_value):
    result = []
    global_max = np.max(I)
    min_value = min_value * global_max
    for i in range(1, I.shape[0]):
        for j in range(1, I.shape[1]):
            neighbors = I[i-1:i+2, j-1:j+2]
            if (np.max(neighbors) == I[i, j]):
                if(I[i][j] > min_value):
                    result.append((i, j))
    return result


def H(I, size_sobel, size_gauss, sigma_gauss):
    sobel_x = cv2.Sobel(I, cv2.CV_32F, 1, 0, ksize=size_sobel)
    sobel_y = cv2.Sobel(I, cv2.CV_32F, 0, 1, ksize=size_sobel)

    I_xx = sobel_x * sobel_x
    I_yy = sobel_y * sobel_y
    I_xy = sobel_x * sobel_y

    size_gauss_tuple = (size_gauss, size_gauss)
    I_xx = cv2.GaussianBlur(I_xx, size_gauss_tuple, sigma_gauss)
    I_yy = cv2.GaussianBlur(I_yy, size_gauss_tuple, sigma_gauss)
    I_xy = cv2.GaussianBlur(I_xy, size_gauss_tuple, sigma_gauss)

    det_M = I_xx * I_yy - I_xy * I_xy
    tr_M = I_xx + I_yy

    k = 0.05
    H = det_M - k * tr_M * tr_M
    max_loc = localMaxima(H, 0.001)

    return H