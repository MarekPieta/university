import cv2
import numpy as np


def draw_flow(img, u, v, step, thresh, color):
    y, x = img.shape
    mm = (u*u+v*v)**0.5
    m = mm>thresh
    for j in range(0,y,step):
        for i in range (0,x,step):
            if m[j][i]:
                cv2.line(img, (i,j), (i+np.int32(u[j][i]), j+np.int32(v[j][i])), color)


f = open('data/highway/temporalROI.txt', 'r')
line = f.readline()
roi_start, roi_end = line.split()
roi_start = int(roi_start)
roi_end = int(roi_end)

i_start = roi_start
i_end = roi_end
i_step = 7

TP = 0
TN = 0
FP = 0
FN = 0

i_start = 100

I = cv2.imread('data/highway/input/in' + str('{:06d}'.format(i_start)) + '.jpg')
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

for i in range(i_start, i_end, i_step):
    I_before = I
    I_color = cv2.imread('data/highway/input/in' + str('{:06d}'.format(i)) + '.jpg')
    I = cv2.cvtColor(I_color, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(I_before, I, None, 0.4, 1, 12, 2, 8, 1.2, 0)
    I_res = I
    u = flow[:, :, 0]
    v = flow[:, :, 1]
    draw_flow(I_res, u, v, 5, 10, [0, 255, 0])

    cv2.imshow("Result", I_res)
    cv2.waitKey(100)