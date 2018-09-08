import math                                     # do PI
from mpl_toolkits.mplot3d import Axes3D         # do 3D
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Generowanie Gaussa
kernel_size = 25                      # rozmiar rozkladu
sigma = 10                           # odchylenie std
x = np.arange(0, kernel_size, 1, float)     # wektor poziomy
y = x[:,np.newaxis]                  # wektor pionowy
x0 = y0 = kernel_size // 2                  # wsp. srodka
G = 1/(2*math.pi*sigma**2)*np.exp(-0.5*((x-x0)**2 + (y-y0)**2) / sigma**2)
# Rysowanie
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, G, color='b')
#plt.show()


# Pochodne
G_y = np.diff(G,1,0);
#Sledzenie obiektow
G_y = np.append(G_y,np.zeros((1,kernel_size),float),0)    # dodanie dodatkowego wiersza
G_y = -G_y
G_x = np.diff(G,1,1);
G_x = np.append(G_x,np.zeros((kernel_size,1),float),1)    # dodanie dodatkowej kolumny
G_x = -G_x


def track_init(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX, mouseY = x, y


def calculate_hyst(I_H, x, y):
    hist_q = np.zeros((256, 1), float)
    for jj in range(0, kernel_size):
        for ii in range(0, kernel_size):
            pixel_H = I_H[y+jj, x+ii];
            hist_q[pixel_H] = hist_q[pixel_H] + pixel_H*G[jj, ii]
    return hist_q


# Wczytanie pierwszego obrazka
I = cv2.imread('data/track00100.png')
cv2.namedWindow('Tracking')
#cv2.setMouseCallback('Tracking',track_init)
x, y = 810, 410
I_YCrCb = cv2.cvtColor(I, cv2.COLOR_BGR2YCR_CB)
I_Cr = I_YCrCb[:, :, 1]

hist_p = calculate_hyst(I_Cr, x, y)

# Pobranie klawisza
for i in range(101, 201):
    cv2.rectangle(I, (x, y), (x + kernel_size, y + kernel_size), (0, 255, 0), 2)
    cv2.imshow('Tracking', I)
    I = cv2.imread('data/track' + str('{:05d}'.format(i)) + '.png')
    I_YCrCb = cv2.cvtColor(I, cv2.COLOR_BGR2YCR_CB)
    I_Cr = I_YCrCb[:, :, 1]

    dx_l = 0
    dx_m = 0
    dy_l = 0
    dy_m = 0

    iterations = 20

    for i in range(0, iterations):
        hist_q = calculate_hyst(I_Cr, x, y)
        rho = np.sqrt(hist_q * hist_p)
        for jj in range(0, kernel_size):
            for ii in range(0, kernel_size):
                dx_l = dx_l + ii*rho[I_Cr[y + jj, x + ii]]*G_x[jj, ii]
                dx_m = dx_m + ii*G_x[jj, ii]
                dy_l = dy_l + jj*rho[I_Cr[y + jj, x + ii]]*G_y[jj, ii]
                dy_m = dy_m + jj*G_y[jj, ii]
        dx = dx_l / dx_m
        dy = dy_l / dy_m
        # Obliczanie nowych wspolrzednych
        x = np.int(np.floor(x + dx))
        y = np.int(np.floor(y + dy))

    cv2.putText(I, str(sum(rho)), (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 2, cv2.LINE_AA)


    cv2.waitKey(20)
