import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets

from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

RANDOM_STATE = 1

np.set_printoptions(precision=2)

#%% Load the dataset.

X, y = datasets.load_wine(return_X_y=True)

#%% Define classifiers and classifier ensembles.

clf1 = DecisionTreeClassifier(random_state=1, min_samples_leaf=3)
clf2 = BaggingClassifier(random_state=1, n_estimators=50)
clf3 = AdaBoostClassifier(random_state=1, n_estimators=50, algorithm='SAMME')
clf4 = GradientBoostingClassifier(random_state=1, min_samples_leaf=3, n_estimators=50, max_depth=1, subsample=0.5, learning_rate=1)


#%% Compare performance of the models.

score1 =  cross_val_score(clf1, X, y, cv=5)
score2 = cross_val_score(clf2, X, y, cv=5)
score3 = cross_val_score(clf3, X, y, cv=5)
score4 = cross_val_score(clf4, X, y, cv=5)

#%% Plot OOB estimates for Gradient Boosting Classifier.

print("Scores:")
print("Decision tree: ",end='')
print(score1,end='')
print (" avg: ", end='')
print(np.mean(score1))
print("Bagging classifier: ",end='')
print(score2,end='')
print (" avg: ", end='')
print(np.mean(score2))
print("Adaboost classifier: ",end='')
print(score3,end='')
print (" avg: ", end='')
print(np.mean(score3))
print("Gradient Boosting classifier: ",end='')
print(score4,end='')
print (" avg: ", end='')
print(np.mean(score4))

clf4.fit(X,y)
plt.plot(np.cumsum(clf4.oob_improvement_))
plt.show()
