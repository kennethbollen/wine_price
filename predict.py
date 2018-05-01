#!python3

from data_extract import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classfication_report
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

