import pickle
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

f = open('hog.pckl', 'rb')
HOG_data = pickle.load(f)
f.close()

y = HOG_data[:, 0]
X = HOG_data[:, 1:HOG_data.shape[1]]


clf = svm.SVC(kernel='linear', C = 1.0)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_validation, X_test, y_validation, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)


clf.fit(X_train, y_train)

y_train_pred = clf.predict(X_train)
cm = confusion_matrix(y_train, y_train_pred)
TP = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
TN = cm[1][1]
ACC = (TP + TN) / (TP + TN + FP + FN)
print('ACC train:')
print(ACC)

y_validation_pred = clf.predict(X_validation)
cm = confusion_matrix(y_validation, y_validation_pred)
TP = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
TN = cm[1][1]
ACC = (TP + TN) / (TP + TN + FP + FN)
print('ACC validation:')
print(ACC)

y_test_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_test_pred)
TP = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
TN = cm[1][1]
ACC = (TP + TN) / (TP + TN + FP + FN)
print('ACC test:')
print(ACC)

f = open ('classifier.pckl', 'wb')
pickle.dump(clf, f)
f.close()