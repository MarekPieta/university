import numpy as np
import cv2
import matplotlib.pyplot as plt

I = cv2.imread('data/I.jpg')
J = cv2.imread('data/J.jpg')
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
J = cv2.cvtColor(J, cv2.COLOR_BGR2GRAY)
diff = cv2.absdiff(I, J)

u = np.zeros(I.shape, np.int8)
v = np.zeros(I.shape, np.int8)

W2 = 1
dX = 1
dY = 1

for j in range(2*W2, I.shape[0]-2*W2):
    for i in range(2*W2, I.shape[1]-2*W2):
        IO = np.float32(I[j - W2:j + W2 + 1, i - W2:i + W2 + 1])
        dd = np.ones((2*dY + 1, 2*dX + 1), np.float64)*np.inf
        for j1 in range(-dX, dX+1):
            for i1 in range(-dY, dY+1):
                JO = np.float32(J[j - W2 + j1:j + W2 + 1 + j1, i - W2 + i1:i + W2 + 1 + i1])
                dd[j1+dX, i1+dY] = np.sum(np.sqrt((np.square(JO - IO))))
        ind = np.unravel_index(np.argmin(dd, axis=None), dd.shape)
        u[j, i] = ind[0]-dX
        v[j, i] = ind[1]-dY


cv2.imshow("I", I)
cv2.imshow("J", J)
cv2.imshow("Diff:", diff)

plt.imshow(I);
plt.quiver(u, v, scale=0.3, scale_units='dots') #minus - axis are inverted
plt.show()

cv2.waitKey(0)