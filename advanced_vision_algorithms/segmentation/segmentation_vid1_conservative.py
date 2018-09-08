import cv2
import numpy as np

I = cv2.imread('seq/office/input/in000300.jpg')
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

f = open('seq/office/temporalROI.txt', 'r')
line = f.readline()
roi_start, roi_end = line.split()
roi_start = int(roi_start)
roi_end = int(roi_end)

i_start = roi_start
i_end = roi_end
i_step = 5

TP = 0
TN = 0
FP = 0
FN = 0

alfa = 0.01
BUF = np.zeros((I.shape[0], I.shape[1]), np.double)
BUF = np.double(I)
iN = 0

for i in range(i_start, i_end, i_step):
    ground_truth = cv2.imread('seq/office/groundtruth/gt' + str('{:06d}'.format(i)) + '.png')
    I_before = I
    I_color = cv2.imread('seq/office/input/in' + str('{:06d}'.format(i)) + '.jpg')
    I = cv2.cvtColor(I_color, cv2.COLOR_BGR2GRAY)
    ground_truth = cv2.cvtColor(ground_truth, cv2.COLOR_BGR2GRAY)
    ground_truth_binary = np.uint8(255*(ground_truth == 255))

    diff = cv2.absdiff(I, np.uint8(BUF))
    thresh, I_binary = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    I_binary = cv2.medianBlur(I_binary, 5)
    BUF[I_binary == 0] = alfa*np.double(I[I_binary==0]) + (1-alfa)*BUF[I_binary==0]

    TP_M = np.logical_and((I_binary == 255), (ground_truth_binary == 255))  # iloczyn
    TP += np.sum(TP_M)
    FP_M = np.logical_and((I_binary == 255), (ground_truth_binary != 255))  # iloczyn
    FP += np.sum(FP_M)
    TN_M = np.logical_and((I_binary != 255), (ground_truth_binary != 255))  # iloczyn
    TN += np.sum(TN_M)
    FN_M = np.logical_and((I_binary != 255), (ground_truth_binary == 255))  # iloczyn
    FN += np.sum(FN_M)

    cv2.imshow("Groundtruth", ground_truth_binary)
    cv2.imshow("Result", I_binary)
    cv2.waitKey(10)

P = TP/(TP+FP)
R = TP/(TP+FN)
F1 = (2*P*R)/(P+R)
print("Stats: ")
print("P: %5.3f." %P)
print("R: %5.3f." %R)
print("F1: %5.3f." %F1)

