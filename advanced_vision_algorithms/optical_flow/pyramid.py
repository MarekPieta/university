import numpy as np
import cv2
import matplotlib.pyplot as plt


def of(I, J, u0, v0, W2=1, dY=1, dX=1):
    u = np.zeros(I.shape, np.int8)
    v = np.zeros(I.shape, np.int8)

    for j in range(2*W2, I.shape[0]-2*W2):
        for i in range(2*W2, I.shape[1]-2*W2):
            IO = np.float32(I[j - W2:j + W2 + 1, i - W2:i + W2 + 1])
            dd = np.ones((2*dY + 1, 2*dX + 1), np.float64)*np.inf
            for j1 in range(-dX, dX+1):
                for i1 in range(-dY, dY+1):
                    JO = np.float32(J[j - W2 + j1 + u0[j, i]:j + W2 + 1 + j1 + u0[j, i], i - W2 + i1 + v0[j, i]:i + W2 + 1 + i1 + v0[j, i]])
                    dd[j1+dX, i1+dY] = np.sum(np.sqrt((np.square(JO - IO))))
            ind = np.unravel_index(np.argmin(dd, axis=None), dd.shape)
            u[j, i] = ind[0]-dX + u0[j, i]
            v[j, i] = ind[1]-dY + v0[j, i]

    return u, v;


def pyramid(im, max_scale):
    images = [im];
    for k in range(1, max_scale):
        images.append(cv2.resize(images[k-1], (0, 0), fx=0.5, fy=0.5))#, interpolation=cv2.INTER_NEAREST))
    return images


I = cv2.imread('data/I.jpg')
J = cv2.imread('data/J.jpg')
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
J = cv2.cvtColor(J, cv2.COLOR_BGR2GRAY)

max_scale = 3
IP = pyramid(I, max_scale)
JP = pyramid(J, max_scale)

u0 = np.zeros(IP[-1].shape, np.int8)
v0 = np.zeros(JP[-1].shape, np.int8)

for i in range(1, max_scale+1):
    u, v = of(IP[-i], JP[-i], u0, v0, W2=1, dY=1, dX=1)
    v0 = cv2.resize(v, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    u0 = cv2.resize(u, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)


plt.imshow(J)
plt.quiver(u, v)#, scale=0.3, scale_units='dots')
plt.show()

cv2.waitKey(0)