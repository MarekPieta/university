# -*- coding: utf-8 -*-
"""

    TOPIC: K-fold Cross-validation

"""

from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

#%%
dataset = datasets.load_iris()
X_all = dataset.data
y_all = dataset.target
number_of_splits = 5


skf = StratifiedKFold(n_splits=number_of_splits, random_state=1)

scores = []
for train_index, test_index in skf.split(X_all, y_all):
    X_train, X_test = X_all[train_index], X_all[test_index]
    y_train, y_test = y_all[train_index], y_all[test_index]
    model = LogisticRegression()
    fmodel = model.fit(X_train, y_train)
    scores.append((model.score(X_test, y_test)))
print(scores)
