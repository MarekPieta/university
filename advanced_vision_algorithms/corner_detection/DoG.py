import cv2
import numpy as np
import matplotlib.pyplot as plt


def create_DoG(I, sigma, k, iterations):
    result = []
    for i in range(1, iterations + 1):
        I1 = cv2.GaussianBlur(I, (5, 5), sigma * k**(i-1))
        I2 = cv2.GaussianBlur(I, (5, 5), sigma * k**i)
        diff = I1 - I2
        result.append(diff)
    return result


def find_max_in_DoG(DoG, thresh):
    result = []
    for s in range(2, len(DoG) - 1):
        for i in range(2, DoG[s].shape[0]):
            for j in range(2, DoG[s].shape[1]):
                neighbor1 = DoG[s-1][i-1:i+2, j-1:j+2]
                neighbor2 = DoG[s][i - 1:i + 2, j - 1:j + 2]
                neighbor3 = DoG[s+1][i - 1:i + 2, j - 1:j + 2]
                neighbors = np.copy(np.dstack((neighbor1, neighbor2, neighbor3)))
                neighbors[1, 1, 1] = -np.inf
                if DoG[s][i, j] > np.max(neighbors):
                    if DoG[s][i, j] > thresh:
                        result.append([j, i, s])
    return result


def show_DoG(I, points, title):
    t = max([el[2] for el in points])
    for i in range(0, t):
        if len(list(filter(lambda x: x[2] == i, points))) == 0:
            continue
        plt.figure()
        plt.title(title + ' ' + str(i))
        plt.gray()
        plt.imshow(I)
        tmp = list(filter(lambda x: x[2] == i, points))
        plt.plot([el[0] for el in tmp], [el[1] for el in tmp], '*r')
        plt.show()
        cv2.waitKey(2000)


f1 = cv2.imread('data/fontanna1.jpg')
f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
fp = cv2.imread('data/fontanna_pow.jpg')
fp = cv2.cvtColor(fp, cv2.COLOR_BGR2GRAY)

f1 = np.float32(f1)
fp = np.float32(fp)

DoG1 = create_DoG(f1, 1.6, 1.26, 5)
extrems1 = find_max_in_DoG(DoG1, 0.002)
DoG2 = create_DoG(fp, 1.6, 1.26, 15)
extrems2 = find_max_in_DoG(DoG2, 0.00002)

show_DoG(f1, extrems1, 'Fontanna1')
show_DoG(fp, extrems2, 'Fontanna Pow')