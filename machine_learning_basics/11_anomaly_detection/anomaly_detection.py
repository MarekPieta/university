import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy import stats


def estimate_gaussian(X):
    mu = 1/X.size * sum(X)
    sigma = 1/X.size * sum((X - mu)**2)

    return mu, sigma


def select_threshold(pval, yval):
    p_min = 0
    p_max = 1

    number_of_steps = 300

    step = (p_max-p_min)/number_of_steps
    best_f1 = 0
    best_epsilon = [0, 0]

    for i in range(0, number_of_steps):
        epsilon1 = p_min + i * step
        for j in range(0, number_of_steps):
            epsilon2 = p_min + j * step
            tp = sum((1 * ((pval[:, 0] < epsilon1) | (pval[:, 1] < epsilon2)) & np.squeeze(yval)))
            tn = sum((1 * ((pval[:, 0] >= epsilon1) & (pval[:, 1] >= epsilon2)) & ~np.squeeze(yval)))
            fp = sum((1 * ((pval[:, 0] < epsilon1) | (pval[:, 1] < epsilon2)) & ~np.squeeze(yval)))
            fn = sum((1 * ((pval[:, 0] >= epsilon1) & (pval[:, 1] >= epsilon2)) & np.squeeze(yval)))

            prec = tp/(tp + fp)
            rec = tp/(tp + fn)
            F = 2*prec*rec/(prec+rec)

            if F > best_f1:
                best_f1 = F
                best_epsilon = [epsilon1, epsilon2]

    return best_epsilon, best_f1


data = loadmat('ex8data1.mat')
X = data['X']
number_of_examples, number_of_features = X.shape
plt.figure(1)
plt.scatter(X[:, 0], X[:, 1])
plt.figure(2)
plt.hist(X[:, 0])
plt.figure(3)
plt.hist(X[:, 1])

mu1, sigma1 = estimate_gaussian(X[:, 0])
mu2, sigma2 = estimate_gaussian(X[:, 1])

Xval = data['Xval']
yval = data['yval']

print("Xval shape: ")
print(Xval.shape)
print("yval shape: ")
print(yval.shape)

p = np.zeros((X.shape[0], X.shape[1]))
p[:, 0] = stats.norm.pdf(X[:, 0], mu1, sigma1)
p[:, 1] = stats.norm.pdf(X[:, 1], mu2, sigma2)

pval = np.zeros((Xval.shape[0], Xval.shape[1]))
pval[:, 0] = stats.norm.pdf(Xval[:, 0], mu1, sigma1)
pval[:, 1] = stats.norm.pdf(Xval[:, 1], mu2, sigma2)

best_epsilon, best_f1 = select_threshold(pval, yval)

anomaly = Xval[np.union1d(np.where(pval[:, 0] < best_epsilon[0]), np.where(pval[:, 1] < best_epsilon[1])), :]
nonanomaly = Xval[np.intersect1d(np.where(pval[:, 0] >= best_epsilon[0]), np.where(pval[:, 1] >= best_epsilon[1])), :]
anomaly_test = yval[np.union1d(np.where(pval[:, 0] < best_epsilon[0]), np.where(pval[:, 1] < best_epsilon[1]))]
nonanomaly_test = yval[np.intersect1d(np.where(pval[:, 0] >= best_epsilon[0]), np.where(pval[:, 1] >= best_epsilon[1]))]

plt.figure(4)
plt.scatter(anomaly[:, 0], anomaly[:, 1], c='r')
plt.scatter(nonanomaly[:, 0], nonanomaly[:, 1])


plt.show()