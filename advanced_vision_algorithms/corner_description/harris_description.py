import cv2
import numpy as np
import matplotlib.pyplot as plt
from harris import H, localMaxima
from pm import plot_matches
import time

def corner_description(image_bw, points, neighborhood_size):
    X, Y = image_bw.shape
    neighborhood = []
    points = list(filter(lambda yx: yx[0] >= neighborhood_size and \
                                    yx[0] < X - neighborhood_size and \
                                    yx[1] >= neighborhood_size and \
                                    yx[1] < Y - neighborhood_size, \
                                    points ))
    for p in points:
        n = image_bw[p[0]-neighborhood_size:p[0]+neighborhood_size+1, p[1]-neighborhood_size:p[1]+neighborhood_size+1]
        n = n.flatten()
        neighborhood.append(n)

    points = list(zip(neighborhood, points))
    return points

def points_comparison(points1, points2, N):
    matched_points = []
    for p1 in points1:
        tested_matching = []
        for p2 in points2:
            tested_matching.append([p2, sum(abs((p1[0] - p2[0])))])

        tested_matching = sorted(tested_matching, key=lambda t: t[1])
        matched_points.append([p1, tested_matching[0][0], tested_matching[0][1]])

    matched_points = sorted(matched_points, key=lambda pointss: pointss[2])

    result = []
    for i in range(0,N):
        p = matched_points[i]
        p_1 = p[0][1]
        p_2 = p[1][1]
        result.append([p_1, p_2])
    return result

def points_comparison_adjust_brightness(points1, points2, N):
    matched_points = []
    for p1 in points1:
        tested_matching = []
        mean_p1 = np.mean(p1[0])
        std_p1 = np.std(p1[0])
        p1_normed = (p1[0] - mean_p1)/std_p1
        for p2 in points2:
            mean_p2 = np.mean(p2[0])
            std_p2 = np.std(p2[0])
            p2_normed = (p2[0] - mean_p2) / std_p2
            tested_matching.append([p2, sum(abs((p1_normed - p2_normed)))])

        tested_matching = sorted(tested_matching, key=lambda t: t[1])
        matched_points.append([p1, tested_matching[0][0], tested_matching[0][1]])

    matched_points = sorted(matched_points, key=lambda pointss: pointss[2])

    result = []
    for i in range(0,N):
        p = matched_points[i]
        p_1 = p[0][1]
        p_2 = p[1][1]
        result.append([p_1, p_2])
    return result


# b1 = cv2.imread('data/fontanna1.jpg')
# b1 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
# H1 = H(b1, 7, 7, 0)
# points1 = localMaxima(H1, 0.2)
# points1 = corner_description(b1, points1, 7)
#
# b2 = cv2.imread('data/fontanna2.jpg')
# b2 = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)
# H2 = H(b2, 7, 7, 0)
# points2 = localMaxima(H2, 0.2)
# points2 = corner_description(b2, points2, 7)
#
# res = points_comparison(points1, points2, 20)
# plot_matches(b1, b2, res)

#################################################

# b1 = cv2.imread('data/budynek1.jpg')
# b1 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
# H1 = H(b1, 7, 7, 0)
# points1 = localMaxima(H1, 0.2)
# points1 = corner_description(b1, points1, 7)
#
# b2 = cv2.imread('data/budynek2.jpg')
# b2 = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)
# H2 = H(b2, 7, 7, 0)
# points2 = localMaxima(H2, 0.2)
# points2 = corner_description(b2, points2, 7)
#
# res = points_comparison(points1, points2, 20)
# plot_matches(b1, b2, res)

##########################################

# b1 = cv2.imread('data/fontanna1.jpg')
# b1 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
# H1 = H(b1, 7, 7, 0)
# points1 = localMaxima(H1, 0.2)
# points1 = corner_description(b1, points1, 7)
#
# b2 = cv2.imread('data/fontanna_pow.jpg')
# b2 = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)
# H2 = H(b2, 7, 7, 0)
# points2 = localMaxima(H2, 0.2)
# points2 = corner_description(b2, points2, 7)
#
# res = points_comparison(points1, points2, 20)
# plot_matches(b1, b2, res)

b1 = cv2.imread('data/eiffel1.jpg')
b1 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
H1 = H(b1, 7, 7, 0)
points1 = localMaxima(H1, 0.2)
points1 = corner_description(b1, points1, 7)

b2 = cv2.imread('data/eiffel2.jpg')
b2 = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)
H2 = H(b2, 7, 7, 0)
points2 = localMaxima(H2, 0.2)
points2 = corner_description(b2, points2, 7)

res = points_comparison(points1, points2, 20)
plot_matches(b1, b2, res)


b1 = cv2.imread('data/eiffel1.jpg')
b1 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
H1 = H(b1, 7, 7, 0)
points1 = localMaxima(H1, 0.2)
points1 = corner_description(b1, points1, 7)

b2 = cv2.imread('data/eiffel2.jpg')
b2 = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)
H2 = H(b2, 7, 7, 0)
points2 = localMaxima(H2, 0.2)
points2 = corner_description(b2, points2, 7)

res = points_comparison_adjust_brightness(points1, points2, 20)
plot_matches(b1, b2, res)
