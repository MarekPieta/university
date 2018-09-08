import numpy as np
import cv2

I_color = cv2.imread('seq/img_seq/in%06d.jpg' % 300)
I = cv2.cvtColor(I_color, cv2.COLOR_BGR2GRAY)

for i in range (301, 450):
    I_before = I
    I_color = cv2.imread('seq/img_seq/in%06d.jpg' % i)
    I = cv2.cvtColor(I_color, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(I, I_before)
    thresh, binary = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    binary = cv2.medianBlur(binary, 5)
    binary = cv2.dilate(binary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 5)), iterations=5)
    binary = cv2.dilate(binary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

    if stats.shape[0] > 1:  # czy sa jakies obiekty
        pi, p = max(enumerate (stats[1:, 4]), key=(lambda x: x[1]))
        pi = pi + 1
    # wyrysownie bbox
        cv2.rectangle(I_color, (stats[pi, 0], stats[pi, 1]), (stats[pi, 0] + stats[pi, 2], stats[pi, 1] + stats[pi, 3]), (0, 0, 255), 2)
    # wypisanie informacji
        cv2.putText(I_color, "%f" % stats[pi, 4], (stats[pi, 0], stats[pi, 1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        cv2.putText(I_color, "%d" % pi, (np.int(centroids[pi, 0]), np.int(centroids[pi, 1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

    cv2.imshow("I", I_color)

    cv2.waitKey(10)