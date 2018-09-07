import cv2 as cv2

def SIFT (b1, b2, name):
    SIFT = cv2.xfeatures2d.SIFT_create()
    b1 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
    points1, descriptors1 = SIFT.detectAndCompute(b1, None)

    b2 = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)
    points2, descriptors2 = SIFT.detectAndCompute(b2, None)

    bf = cv2.BFMatcher()

    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    best_matches = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            best_matches.append([m])

    result = cv2.drawMatchesKnn(b1, points1, b2, points2, best_matches, None, flags=2)
    cv2.imshow(name, result)




b1 = cv2.imread('data/fontanna1.jpg')
b2 = cv2.imread('data/fontanna2.jpg')
SIFT(b1, b2, 'Fontanna')

b1 = cv2.imread('data/fontanna1.jpg')
b2 = cv2.imread('data/fontanna_pow.jpg')
SIFT(b1, b2, 'Fontanna pow')


b1 = cv2.imread('data/budynek1.jpg')
b2 = cv2.imread('data/budynek2.jpg')
SIFT(b1, b2, 'Budynek')

b1 = cv2.imread('data/eiffel1.jpg')
b2 = cv2.imread('data/eiffel2.jpg')
SIFT(b1, b2, 'Eiffel')

cv2.waitKey(0)
