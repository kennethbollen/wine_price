#!python3

from data_extract import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
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
y_pred = svm.predict(X_test)

#confusion matrix results
confusion = confusion_matrix(y_test, y_pred)
print('confusion matrix: {}'.format(confusion))

#determine optimal precision recall with curve for classification report
precision, recall, thresholds = precision_recall_curve(y_test, svm.decision_function(X_test))
close_zero = np.argmin(np.abs(thresholds))
plt.plot(precision[close_zero], recall[close_zero], marker='o', label='threshold at zero', fillstyle='none', c='k', mew=2)
plt.plot(precision, recall, label='precision-recall curve')
plt.xlabel('precision')
plt.ylabel('recall')
plt.title('Precision recall curve for classes: Good wine vs. Bad wine')
plt.legend(loc='best')

#the defualt threshold will have points greater than 0 classified into class 1
#This is an imbalanced dataset with more 1s than 0s
#I want to increase the precision of finding 0s and therefore increase the threshold from 0 to be less bias to 1

y_pred_higher_threshold = svm.decision_function(X_test) > .2
print('Classification report: {}'.format(classification_report(y_test, y_pred_higher_threshold)))

#create a function to predict user satisfaction
def predict_wine(price, wine, country):
	#array to capture prediction
	y_predict = np.empty(19)
	
	#This will scale the data from the format of the user input into how the model reads the data (binary intergers)
	fine_wine = 0
	red_wine = 0
	white_wine = 0
	rose_wine = 0
	argentina = 0
	australian = 0
	chilean = 0
	french = 0
	italian = 0
	new_zealand = 0
	portuguese = 0
	south_african = 0
	spanish = 0
	zero_ten = 0
	eleven_thirty = 0
	thirtyone_fifty = 0
	fiftyone_hundered = 0
	hunderedone_twofifty = 0
	twofiftyone_fivehundered = 0
	
	#the price argument
	if price <= 10:
		zero_ten += 1
	elif price <= 30:
		eleven_thirty += 1
	elif price <= 50:
		thirtyone_fifty += 1
	elif price <= 100:
		fiftyone_hundered += 1
	elif price <= 250:
		twofiftyone_fivehundered += 1
	else:
		print('price is out of range, please input a lower price')
	
	#the wine argument
	if wine.lower() == 'fine wine' or wine.lower() == 'fine_wine' or wine.lower() == 'fine':
		fine_wine += 1
	elif wine.lower() == 'red wine' or wine.lower() == 'red_wine' or wine.lower() == 'red':
		red_wine += 1
	elif wine.lower() == 'white wine' or wine.lower() == 'white_wine' or wine.lower() == 'white':
		white_wine += 1
	elif wine.lower() == 'rose wine' or wine.lower() == 'rose_wine' or wine.lower() == 'rose':
		rose_wine += 1
	else:
		print('wine selected not in the database, please choose: white, red, rose or fine wine')
	
	#the country argument
	if country.lower() == 'argentina':
		argentina += 1
	elif country.lower() == 'australian' or country.lower() == 'australia':
		australian += 1
	elif country.lower() == 'chilean' or country.lower() == 'chile':
		chilean += 1
	elif country.lower() == 'french' or country.lower() == 'france':
		french += 1
	elif country.lower() == 'italian' or country.lower() == 'italy':
		italian += 1
	elif country.lower() == 'new zealand' or country.lower() == 'new zealand':
		new_zealand += 1
	elif country.lower() == 'portuguese' or country.lower() == 'portugal':
		portuguese += 1
	elif country.lower() == 'south african' or country.lower() == 'south_african' or country.lower() == 'south africa' or country.lower() == 'south_africa':
		south_african += 1
	elif country.lower() == 'spanish' or country.lower() == 'spain':
		spanish += 1
	else:
		print('does not recognize the country, please input valid country')

	#create a list of the inputed data in the same order as how the prediction model was trained from the dataset
	attr = [fine_wine, red_wine, rose_wine, white_wine, argentina, australian, chilean, french, italian, new_zealand, portuguese, south_african, spanish, zero_ten, eleven_thirty, thirtyone_fifty, fiftyone_hundered, hunderedone_twofifty, twofiftyone_fivehundered]
  	
	#append the prediction variable with the independent variables stored in the attr list
	for i in attr:
		np.append(y_predict, i)
	y_predict = y_predict.reshape(1, -1)
	#make a prediction
	result = svm.predict(y_predict)
	#translate the prediction
	if result == 1:
		print('This wine will be favourable with customers')
	elif result == 0:
		print('This wine will be unfavoruable with customers')
	else:
		print('unknown...check inputs')
