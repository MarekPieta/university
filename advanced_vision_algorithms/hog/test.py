import cv2
import numpy as np
from hog import hog
import pickle


def detect(im, size, clf):
    im = cv2.resize(im, (int(im.shape[1]*size), int(im.shape[0]*size)))
    im_rows, im_cols, colors = im.shape
    result = im

    template_cols = 64
    template_rows = 128

    step = 4
    for i in range(0, im_cols-template_cols, step):
        for j in range(0, im_rows - template_rows, step):
            tested_im = im[j:j+template_rows, i:i+template_cols]
            hogg = hog(tested_im)
            if clf.predict(hogg.reshape(1, -1)) == 1:
                cv2.rectangle(result,(i, j), (i+template_cols, j+template_rows), (0, 255, 0))
    return result


f = open('classifier.pckl', 'rb')
clf = pickle.load(f)
f.close()

images = []
numberOfImages = 4
for i in range(1, numberOfImages+1):
    images.append(cv2.imread('data/testImages/testImage' + str(i) + '.png'))



res = detect(images[0], 0.65, clf)
cv2.imwrite('res0.png', res)
cv2.waitKey(0)