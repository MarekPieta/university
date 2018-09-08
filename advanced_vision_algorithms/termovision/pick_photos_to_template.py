import cv2
import numpy as np

cap = cv2.VideoCapture('data/vid1_IR.avi')
iPedestrian = 0
temp_counter = 0

while cap.isOpened():
    ret, frame = cap.read()
    if frame is None:
        break
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
                roi = G[i[cv2.CC_STAT_TOP]:i[cv2.CC_STAT_TOP] + i[cv2.CC_STAT_HEIGHT], i[cv2.CC_STAT_LEFT]:i[cv2.CC_STAT_LEFT] + i[cv2.CC_STAT_WIDTH]]
                temp_counter += 1
                if temp_counter % 50 == 0:
                    cv2.imwrite('templates/sample_%06d.png' % iPedestrian, roi)
                    iPedestrian += 1
                    temp_counter = 0

    cv2.imshow('Detected', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()