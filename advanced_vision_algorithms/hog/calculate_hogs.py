import cv2
import numpy as np
from hog import hog
import pickle

HOG_data = np.zeros([2*100,3781],np.float32)
for i in range(0,100):
    IP = cv2.imread('data/pedestrians/pos/per%05d.ppm' %(i+1))
    IN = cv2.imread('data/pedestrians/neg/neg%05d.png' %(i+1))
    F = hog(IP)
    HOG_data[i,0] = 1
    HOG_data[i,1:] = F
    F = hog(IN)
    HOG_data[i+100,0] = 0
    HOG_data[i+100,1:] = F

f = open ('hog.pckl', 'wb')
pickle.dump(HOG_data, f)
f.close()