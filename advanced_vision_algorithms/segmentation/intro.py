import cv2
import numpy as np

I = cv2.imread('seq/img_seq/in000300.jpg')
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

base_number = 300

for i in range(1,150):
    I_before = I
    I_color = cv2.imread('seq/img_seq/in000' + str(base_number + i) + '.jpg')
    I = cv2.cvtColor(I_color, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(I, I_before)
    thresh, binary = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    binary = cv2.medianBlur(binary, 5)
    binary = cv2.dilate(binary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 5)), iterations=4)
    binary = cv2.dilate(binary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

    if stats.shape[0] > 1:
        # czy sa jakies obiekty
        pi, p = max(enumerate(stats[1:, 4]), key=(lambda x: x[1]))
        pi = pi + 1
        # wyrysownie bbox
        cv2.rectangle(I_color, (stats[pi, 0], stats[pi, 1]), (stats[pi, 0] + stats[pi, 2], stats[pi, 1] + stats[pi, 3]), (0, 0, 255), 2)
        # wypisanie informacji
        cv2.putText(I_color, "%f" % stats[pi, 4], (stats[pi, 0], stats[pi, 1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        cv2.putText(I_color, "%d" % pi, (np.int(centroids[pi, 0]), np.int(centroids[pi, 1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

    cv2.imshow("Result", I_color)
    cv2.waitKey(10)