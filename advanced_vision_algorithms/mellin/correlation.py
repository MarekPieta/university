import cv2
import numpy as np
from matplotlib import pyplot

template = cv2.imread('data/wzor.pgm', 0)
im = cv2.imread('data/domek_s80.pgm', 0)
rows, columns = im.shape
rows_template, columns_template = template.shape

start_x = (columns - columns_template) // 2
start_y = (rows - rows_template) // 2

template2 = np.zeros(im.shape)
template2[start_x:(start_x+columns_template), start_y:(start_y+rows_template)] = template
template2 = np.fft.fftshift(template2)

f = np.fft.fft2(im)
f_template = np.fft.fft2(template2)
corr = f*f_template.conj()
#normalization - to get phase correlation
corr = corr/np.abs(corr)
ifft = np.fft.ifft2(corr)

y, x = np.unravel_index(np.argmax(abs(ifft)), ifft.shape)
print(y, x)

template3 = np.zeros(im.shape)

dx = x - template.shape[1]//2
dy = y - template.shape[0]//2
translation_matrix = np.float32([[1,0,dx],[0,1,dy]])

result = cv2.warpAffine(template, translation_matrix, (template2.shape[1], template2.shape[0]))

pyplot.figure(0)
pyplot.imshow(im, cmap='gray')
pyplot.plot([x], [y], 'ro')

pyplot.figure(1)
pyplot.imshow(result, cmap='gray')
pyplot.plot([x], [y], 'ro')
pyplot.show()