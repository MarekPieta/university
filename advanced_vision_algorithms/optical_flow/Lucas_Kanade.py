import cv2
import numpy as np





f = open('data/highway/temporalROI.txt', 'r')
line = f.readline()
roi_start, roi_end = line.split()
roi_start = int(roi_start)
roi_end = int(roi_end)

i_start = roi_start
i_end = roi_end
i_step = 1

TP = 0
TN = 0
FP = 0
FN = 0

feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

i_start = 700

I = cv2.imread('data/highway/input/in' + str('{:06d}'.format(i_start)) + '.jpg')
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

p0 = cv2.goodFeaturesToTrack(I, mask = None, **feature_params)

for i in range(i_start, i_end, i_step):
    I_before = I
    I_color = cv2.imread('data/highway/input/in' + str('{:06d}'.format(i)) + '.jpg')
    I = cv2.cvtColor(I_color, cv2.COLOR_BGR2GRAY)

    p1, st, err = cv2.calcOpticalFlowPyrLK (I_before, I, p0, None)
    draw1 = p0[st == 1] #points to draw
    draw2 = p1[st == 1]

    I_res = cv2.cvtColor(I, cv2.COLOR_GRAY2BGR)

    x1 = np.ravel(draw1[:,0])
    y1 = np.ravel(draw1[:, 1])

    x2 = np.ravel(draw2[:,0])
    y2 = np.ravel(draw2[:,1])
    for i in range(1, len(draw1)):
        cv2.line(I_res, (x1[i], y1[i]), (x2[i], y2[i]), [0, 0, 255])

    p1 = p1[st == 1]
    p0 = p1.reshape(-1, 1, 2)
    cv2.imshow("Result", I_res)
    cv2.waitKey(100)
