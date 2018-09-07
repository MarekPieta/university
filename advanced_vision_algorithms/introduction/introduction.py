import cv2
import numpy as np
import matplotlib.pyplot as plt


def hist(img):
    h=np.zeros((256,1), np.float32) # tworzy i zeruje tablice jednokolumnowa
    height, width =img.shape[:2] # shape - krotka z wymiarami - bierzemy 2 pierwsze
    for y in range(height):
        for x in range(width):
            h[img[x,y] ] += 1
    return h


img = cv2.imread('mandril.jpg')
imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

IH = imgHSV[:,:,0]
IS = imgHSV[:,:,1]
IV = imgHSV[:,:,2]

cv2.imshow("Mandril", img)  # wyswietlenie
cv2.imshow("Mandril - Gray", imgG)  # wyswietlenie
cv2.imshow("Mandril - HSV", imgHSV)  # wyswietlenie


print(img.shape)  # rozmiary /wiersze, kolumny, glebia/
print(img.size)   # liczba bajtow
print(img.dtype)  # typ danych

height, width = img.shape[:2]       # pobranie elementow 1 i 2 tj. odpowienio wysokosci i szerokosci
scale = 1.75                     # wspolczynnik skalujacy
Ix2 = cv2.resize(img,(int(scale*height),int(scale*width)))
cv2.imshow("Big Mandril",Ix2)

lena = cv2.imread('lena.png')
lena_gray = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)

added = np.double(imgG) + np.double(lena_gray)
cv2.imshow("Added lena and mandril - gray images", np.uint8(added))

diff = np.double(imgG) - np.double(lena_gray)
cv2.imshow("Diff: lena and mandril - gray images", np.uint8(diff))

mult = imgG * lena_gray
cv2.imshow("Mult: lena and mandril - gray images", np.uint8(mult))

abs_diff = abs(diff)
cv2.imshow("AbsDiff: lena and mandril - gray images", np.uint8(abs_diff))

lena_hist = hist(lena_gray)
lena_hist2 = cv2.calcHist([lena_gray],[0],None,[256],[0,256])

plt.figure(1)
plt.title('Hist - manually')
plt.plot(lena_hist)

plt.figure(2)
plt.title('Hist - OpenCV')
plt.plot(lena_hist2)

lena_hist_equalised = cv2.equalizeHist(lena_gray)
cv2.imshow('Lena with equalised hist', lena_hist_equalised)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# clipLimit - maksymalna wysokosc slupka histogramu - wartosci powyzej
#rozdzielana sa pomiedzy sasiadow
# tileGridSize - rozmiar pojedycznczego bloku obrazu (metoda lokalna, dziala
#na rozdzielnych blokach obrazu)
lena_clahe = clahe.apply(lena_gray)
cv2.imshow('Lena after CLAHE', lena_clahe)

lena_gaussian_blur = cv2.GaussianBlur(lena_gray, (5,5), 3)
cv2.imshow('Lena after Gaussian blur', lena_gaussian_blur)

lena_sobel = cv2.Sobel(lena_gray, cv2.CV_64F,1,0)
cv2.imshow('Lena after Sobel', lena_sobel)

lena_laplacian = cv2.Laplacian(lena_gray, cv2.CV_64F)
cv2.imshow('Lena after Laplacian', lena_laplacian)

lena_median_blur = cv2.medianBlur(lena_gray, 5)
cv2.imshow('Lena after median blur', lena_median_blur)

cv2.waitKey(0)                # oczekiwanie na klawisz
cv2.destroyAllWindows()       # zamkniecie wszystkich okien

plt.show()