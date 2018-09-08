import cv2
import numpy as np


def join_elements(i,j,stats):
    index = 0
    for ii in range(1, len(stats)):
        if (stats[ii] == j).all():
            index = ii
            break
    if (index != 0):
        stats = np.delete(stats, index)
    return stats


def rectangles_are_close(i, j):
    if abs(i[cv2.CC_STAT_TOP] + i[cv2.CC_STAT_HEIGHT] - j[cv2.CC_STAT_TOP]) < 15:
        if i[cv2.CC_STAT_LEFT] - j[cv2.CC_STAT_LEFT] > -10:
            if (i[cv2.CC_STAT_LEFT] + i[cv2.CC_STAT_WIDTH]) - (j[cv2.CC_STAT_LEFT] + j[cv2.CC_STAT_WIDTH]) < 10:
                if (j[cv2.CC_STAT_WIDTH] < j[cv2.CC_STAT_HEIGHT]):
                    return True

    if abs(i[cv2.CC_STAT_TOP] - (j[cv2.CC_STAT_TOP] + j[cv2.CC_STAT_HEIGHT])) < 15:
        if i[cv2.CC_STAT_LEFT] - j[cv2.CC_STAT_LEFT] > -10:
            if (i[cv2.CC_STAT_LEFT] + i[cv2.CC_STAT_WIDTH]) - (j[cv2.CC_STAT_LEFT] + j[cv2.CC_STAT_WIDTH]) < 10:
                    if (j[cv2.CC_STAT_WIDTH] < j[cv2.CC_STAT_HEIGHT]):
                        return True
    return False

cap = cv2.VideoCapture('data/vid1_IR.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    G = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, G_binary = cv2.threshold(G, 40, 255, cv2.THRESH_BINARY)
    G_binary = cv2.medianBlur(G_binary, 7)

    kernel = np.ones((21, 5), np.uint8)
    G_binary = cv2.dilate(G_binary, kernel)

    output = cv2.connectedComponentsWithStats(G_binary, 8, cv2.CV_32S)
    # number of labels
    num_labels = output[0]
    # label matrix
    labels = output[1]
    # stat matrix
    stats = output[2]
    # centroid matrix
    centroids = output[3]

#    for i in stats:
#        if i[cv2.CC_STAT_HEIGHT] < 100:
#            for j in stats:
#                if rectangles_are_close(i, j):
#                    stats = join_elements(i, j, stats)

    for i in stats:
        if i[cv2.CC_STAT_WIDTH] < i[cv2.CC_STAT_HEIGHT]:
            if i[cv2.CC_STAT_HEIGHT] > 100:
 #               for j in stats:
 #                   if rectangles_are_close(i, j):
 #                       cv2.rectangle(frame, (j[cv2.CC_STAT_LEFT], j[cv2.CC_STAT_TOP]), (j[cv2.CC_STAT_LEFT] + j[cv2.CC_STAT_WIDTH], j[cv2.CC_STAT_TOP] + j[cv2.CC_STAT_HEIGHT]), (0, 0, 255))
                cv2.rectangle(frame, (i[cv2.CC_STAT_LEFT], i[cv2.CC_STAT_TOP]), (i[cv2.CC_STAT_LEFT]+i[cv2.CC_STAT_WIDTH], i[cv2.CC_STAT_TOP]+i[cv2.CC_STAT_HEIGHT]), (0, 255, 0))

    cv2.imshow('Detected', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()