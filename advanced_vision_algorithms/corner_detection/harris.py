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
                    result.append((j, i))
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

b1 = cv2.imread('data/budynek1.jpg')
b1 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)

b2 = cv2.imread('data/budynek2.jpg')
b2 = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)

f1 = cv2.imread('data/fontanna1.jpg')
f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)

f2 = cv2.imread('data/fontanna2.jpg')
f2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)

fp = cv2.imread('data/fontanna_pow.jpg')
fp = cv2.cvtColor(fp, cv2.COLOR_BGR2GRAY)


plt.figure(1)
plt.title('b1: ')
plt.gray()
plt.imshow(b1)
H1 = H(b1, 7, 7, 0)
points = localMaxima(H1, 0.2)
plt.plot([el[0] for el in points], [el[1] for el in points], 'r*')

plt.figure(2)
plt.title('b2: ')
plt.gray()
plt.imshow(b2)
H1 = H(b2, 7, 7, 0)
points = localMaxima(H1, 0.2)
plt.plot([el[0] for el in points], [el[1] for el in points], 'r*')

plt.figure(3)
plt.title('f1: ')
plt.gray()
plt.imshow(f1)
H1 = H(f1, 7, 7, 0)
points = localMaxima(H1, 0.2)
plt.plot([el[0] for el in points], [el[1] for el in points], 'r*')


plt.figure(4)
plt.title('f2: ')
plt.gray()
plt.imshow(f2)
H1 = H(f2, 7, 7, 0)
points = localMaxima(H1, 0.2)
plt.plot([el[0] for el in points], [el[1] for el in points], 'r*')

plt.figure(5)
plt.title('fp: ')
plt.gray()
plt.imshow(fp)
H1 = H(fp, 7, 7, 0)
points = localMaxima(H1, 0.2)
plt.plot([el[0] for el in points], [el[1] for el in points], 'r*')
plt.show()