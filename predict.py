#!python3

from data_extract import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classfication_report
from sklearn.metrics import precision_recall_curve
from sklearn.svm import SVC

#split the data into train, validation and test data
X_trainval, X_test, y_trainval, y_test = train_test_split(X, y, random_state=0)

#split the data into train and validation sets
X_train, X_validation, y_train, y_validation = train_test_split(X_trainval, y_trainval, random_state=0)

#find the best parameters with the validation data set
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 1, 10, 100]}
grid_search = GridSearchCV(SVC(), param_grid, cv=5)
grid_search.fit(X_validation, y_validation)
C_best, gamma_best = grid_search.best_params_.values()

#train the model with the best parameters
svm = SVC(C=C_best, gamma=gamma_best)
svm.fit(X_train, y_train)
print('training score: {:2f}'.format(svm.score(X_train, y_train)))
print('test score: {:2f}'.format(svm.score(X_test, y_test)))

#prediction on unseen data
y_pred = svm.pred(X_test)

#confusion matrix results
confusion = confusion_matrix(y_test, y_pred)
print('confusion matrix: {}'.format(confusion))

#determine optimal precision recall with curve for classification report
precision, recall, thresholds = precision_recall_curve(y_test, svm.decision_function(X_test))
close_zero = np.argmin(np.abs(thresholds))
plt.plot(precision[close_zero], recall[close_zero], market='o', label='threshold at zero', fillstyle='none', c='k', mew=2)
plt.plot(precision, recall, label='precision-recall curve')
plt.xlabel('precision')
plt.ylabel('recall')
plt.title('Precision recall curve for classes: Good wine vs. Bad wine')
plt.label(loc='best')

#the defualt threshold will have points greater than 0 classified into class 1
#This is an imbalanced dataset with more 1s than 0s
#I want to increase the precision of finding 0s and therefore increase the threshold from 0 to be less bias to 1

y_pred_higher_threshold = grid.decision_function(X_test) > .95
print('Classification report: {}'.format(classification_report(y_test, y_pred_higher_threshold)))

