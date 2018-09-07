import cv2
import numpy as np
import matplotlib.pyplot as plt


#  kryternia przetwania obliczen (blad+liczba iteracji)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# przygotowanie punktow 2D w postaci: (0,0,0), (1,0,0), (2,0,0) ....,(6,7,0)
objp_l = np.zeros((6*7, 3), np.float32)
objp_l[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

objp_r = np.zeros((6*7, 3), np.float32)
objp_r[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)


# tablice do przechowywania punktow obiektow (3D) i punktow na obrazie (2D) dla wszystkich obrazow
objpoints_l = [] # punkty 3d w przestrzeni (rzeczywsite)
imgpoints_l = [] # punkty 2d w plaszczyznie obrazu.

objpoints_r = [] # punkty 3d w przestrzeni (rzeczywsite)
imgpoints_r = [] # punkty 2d w plaszczyznie obrazu.


for fname in range(1, 13):
    # wczytanie obrazu
    img_l = cv2.imread('data/images_left/left%02d.jpg' %fname)
    img_r = cv2.imread('data/images_right/right%02d.jpg' % fname)

    # konwersja do odcieni szarosci
    gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
    gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)

    # wyszukiwanie naroznikow na planszy
    ret_l, corners_l = cv2.findChessboardCorners(gray_l, (7, 6), None)
    ret_r, corners_r = cv2.findChessboardCorners(gray_r, (7, 6), None)

    # jesli znaleniono na obrazie punkty
    if ret_l == True and ret_r == True:
        #dolaczenie wspolrzednych 3D
        objpoints_l.append(objp_l)
        # poprawa lokalizacji punktow (podpiskelowo)
        corners2_l = cv2.cornerSubPix(gray_l, corners_l, (11, 11), (-1, -1), criteria)
        # dolaczenie poprawionych punktow
        imgpoints_l.append(corners2_l)
        # wizualizacja wykrytych naroznikow
        cv2.drawChessboardCorners(img_l, (7, 6), corners2_l, ret_l)
        #dolaczenie wspolrzednych 3D
        objpoints_r.append(objp_r)
        # poprawa lokalizacji punktow (podpiskelowo)
        corners2_r = cv2.cornerSubPix(gray_r, corners_r, (11, 11), (-1, -1), criteria)
        # dolaczenie poprawionych punktow
        imgpoints_r.append(corners2_r)
        # wizualizacja wykrytych naroznikow
        cv2.drawChessboardCorners(img_r, (7, 6), corners2_r, ret_r)



ret_l, mtx_l, dist_l, rvecs_l, tvecs_l = cv2.calibrateCamera(objpoints_l, imgpoints_l, gray_l.shape[::-1], None, None)
ret_r, mtx_r, dist_r, rvecs_r, tvecs_r = cv2.calibrateCamera(objpoints_r, imgpoints_r, gray_r.shape[::-1], None, None)


h_l, w_l = img_l.shape[:2]
newcameramtx_l, roi_l = cv2.getOptimalNewCameraMatrix(mtx_l, dist_l, (w_l, h_l), 1, (w_l, h_l))

h_r, w_r = img_r.shape[:2]
newcameramtx_r, roi_r = cv2.getOptimalNewCameraMatrix(mtx_r, dist_r, (w_r, h_r), 1, (w_r, h_r))

for fname in range(1, 13):
    img_l = cv2.imread('data/images_left/left%02d.jpg' % fname)
    gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
    dst_l = cv2.undistort(img_l, mtx_l, dist_l, None, newcameramtx_l)
    x, y, w, h = roi_l
    dst_l = dst_l[y:y+h, x:x+w]
    cv2.imwrite('calibresult_left%02d.png' %fname, dst_l)

for fname in range(1, 13):
    img_r = cv2.imread('data/images_right/right%02d.jpg' % fname)
    gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
    dst_r = cv2.undistort(img_r, mtx_r, dist_r, None, newcameramtx_r)
    x, y, w, h = roi_r
    dst_r = dst_r[y:y+h, x:x+w]
    cv2.imwrite('calibresult_right%02d.png' %fname, dst_r)

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
    cv2.stereoCalibrate(objpoints_r, imgpoints_l, imgpoints_r, mtx_l, dist_l, mtx_r, dist_r, gray_r.shape[::-1])
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = \
    cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, gray_r.shape[::-1], R, T)

map1_l, map2_l = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, P1, gray_l.shape[::-1], cv2.CV_16SC2)
map1_r, map2_r = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2,P2, gray_l.shape[::-1], cv2.CV_16SC2)

img_l = cv2.imread('data/images_left/left01.jpg')
img_r = cv2.imread('data/images_right/right01.jpg')

dst_l = cv2.remap(img_l, map1_l, map2_l, cv2.INTER_LINEAR)
dst_r = cv2.remap(img_r, map1_r, map2_r, cv2.INTER_LINEAR)

N, XX, YY = dst_l.shape[::-1] # pobranie rozmiarow obrazka (kolorowego)
visRectify = np.zeros((YY, XX*2, N), np.uint8) # utworzenie nowego obrazka o szerokosci x2
visRectify[:, 0:640:, :] = dst_l      # przypisanie obrazka lewego
visRectify[:, 640:1280:, :] = dst_r   # przypisanie obrazka prawego
# Wyrysowanie poziomych linii
for y in range(0, 480, 10):
    cv2.line(visRectify, (0, y), (1280, y), (255, 0, 0))
    cv2.imshow('visRectify', visRectify)  #wizualizacja

cv2.waitKey(0)