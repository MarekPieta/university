import cv2
import numpy as np
from matplotlib import pyplot


def hanning2D(n):
    h = np.hanning(n)
    return np.sqrt(np.outer(h,h))


def highpassFilter(size):
    rows = np.cos(np.pi*np.matrix([-0.5 + x/(size[0]-1) for x in range(size[0])]))
    cols = np.cos(np.pi*np.matrix([-0.5 + x/(size[1]-1) for x in range(size[1])]))
    X = np.outer(rows, cols)
    return (1.0 - X) * (2.0 - X)


template = cv2.imread('data/domek_r0_64.pgm', 0)
im = cv2.imread('data/domek_r210.pgm', 0)

rows, columns = im.shape
rows_template, columns_template = template.shape

start_x = (columns - columns_template) // 2
start_y = (rows - rows_template) // 2

template2 = np.zeros(im.shape)
hanning = hanning2D(template.shape[0])
template = template*hanning

template2[start_x:(start_x+columns_template), start_y:(start_y+rows_template)] = template
template2 = np.fft.fftshift(template2)

f = np.fft.fft2(im)
f_temp = np.fft.fft2(template2)

f = np.fft.fftshift(f)
f_temp = np.fft.fftshift(f_temp)

f = np.abs(f)
f_temp = np.abs(f_temp)

highpass1 = highpassFilter(f.shape)
highpass2 = highpassFilter(f_temp.shape)


f = f*highpass1
f_temp = f_temp*highpass2

R = f.shape[0]/2
M = 2*R/np.log(R)
lp = cv2.logPolar(f, (f.shape[0]/2, f.shape[1]/2), M, flags=cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS)

temp_lp = cv2.logPolar(f_temp, (f_temp.shape[0]/2, f_temp.shape[1]/2), M, flags=cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS)


f_lp = np.fft.fft2(lp)
f_temp_lp = np.fft.fft2(temp_lp)

corr_lp = f_lp * f_temp_lp.conj()
corr_lp = corr_lp/np.abs(corr_lp)
ifft = np.fft.ifft2(corr_lp)

angle, logr = np.unravel_index(np.argmax(abs(ifft)), ifft.shape)

if logr > ifft.shape[1] // 2:
    wykl = R - logr
else:
    wykl = -logr

scale = np.exp(1/M) ** wykl

A = (angle * 360.0)/ifft.shape[0]
angle1 = 360-A
angle2 = 360-A-180

midTrans1 = [np.floor((im.shape[0] + 1) / 2), np.floor((im.shape[1] + 1) / 2)]
transformation_matrix1 = cv2.getRotationMatrix2D((midTrans1[0], midTrans1[1]), -angle1, 1)

midTrans2 = [np.floor((im.shape[0] + 1) / 2), np.floor((im.shape[1] + 1) / 2)]
transformation_matrix2 = cv2.getRotationMatrix2D((midTrans2[0], midTrans2[1]), -angle2, 1)

im1 = cv2.warpAffine(im, transformation_matrix1, (im.shape[1], im.shape[0])) #cols, rows
im2 = cv2.warpAffine(im, transformation_matrix2, (im.shape[1], im.shape[0]))

template = cv2.imread('data/wzor.pgm', 0)
rows_template, columns_template = template.shape
start_x = (columns - columns_template) // 2
start_y = (rows - rows_template) // 2

template2 = np.zeros(im.shape)

template2[start_x:(start_x+columns_template), start_y:(start_y+rows_template)] = template
template2 = np.fft.fftshift(template2)

f1 = np.fft.fft2(im1)
f2 = np.fft.fft2(im2)
f_template = np.fft.fft2(template2)

corr1 = f1*f_template.conj()
corr2 = f2*f_template.conj()

#normalization - to get phase correlation
corr1 = corr1/np.abs(corr1)
corr2 = corr2/np.abs(corr2)

ifft1 = np.fft.ifft2(corr1)
ifft2 = np.fft.ifft2(corr2)

if np.max(ifft1) > np.max(ifft2):
    y, x = np.unravel_index(np.argmax(abs(ifft1)), ifft1.shape)
    pyplot.figure(0)
    pyplot.imshow(im1, cmap='gray')
    pyplot.plot([x], [y], 'ro')
    pyplot.show()
else:
    y, x = np.unravel_index(np.argmax(abs(ifft2)), ifft2.shape)
    pyplot.figure(1)
    pyplot.imshow(im2, cmap='gray')
    pyplot.plot([x], [y], 'ro')
    pyplot.show()