from data_extract import *
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state=42)

# Create the classifier: logreg
logreg = LogisticRegression()
# Fit the classifier to the training data
logreg.fit(X_train, y_train)

# Predict the labels of the test set: y_pred
y_pred = logreg.predict(X_test)

# Compute and print the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Compute predicted probabilities: y_pred_prob
y_pred_prob = logreg.predict_proba(X_test)[:,1]

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)

# Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

# Compute predicted probabilities: y_pred_prob
# Returns the probability of a given sample being in a particular class
y_pred_prob = logreg.predict_proba(X_test)[:,1]

# Compute and print AUC score
print("AUC: {}".format(roc_auc_score(y_test, y_pred_prob)))

# Compute cross-validated AUC scores: cv_auc
cv_auc = cross_val_score(logreg,X,y,cv=5,scoring='roc_auc')

# Print list of AUC scores
# if the model is greater than 0.5 than it shows signs that it's a strong model (better than guessing)
print("AUC scores computed using 5-fold cross-validation: {}".format(cv_auc))

# Setup the hyperparameter grid
# C controls the inverse of the regularization strength
# A large C can lead to an overfit model, while a small C can lead to an underfit model
c_space = np.logspace(-5, 8, 15)
param_grid = {'C': c_space}

# Instantiate the GridSearchCV object: logreg_cv
print('finding optimal regularization strength, in this hyperparameter space...')
logreg_cv = GridSearchCV(logreg, param_grid, cv=5)

# Fit it to the data
logreg_cv.fit(X, y)

# Print the tuned parameters and score
print("Tuned Logistic Regression Parameters: {}".format(logreg_cv.best_params_)) 
print("Best score is {}".format(logreg_cv.best_score_))

def predict_wine(price, wine, country):
	y_predict = [price]
	
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
	new_world = 0
	old_world = 0

	try:
		if wine.lower() == 'fine wine' or wine.lower() == 'fine_wine' or wine.lower() == 'fine':
			fine_wine += 1
		elif wine.lower() == 'red wine' or wine.lower() == 'red_wine' or wine.lower() == 'red':
			red_wine += 1
		elif wine.lower() == 'white wine' or wine.lower() == 'white_wine' or wine.lower() == 'white':
			white_wine += 1
		elif wine.lower() == 'rose wine' or wine.lower() == 'rose_wine' or wine.lower() == 'rose':
			rose_wine += 1
		else:
			print('Does not recognize the type of wine, please input (e.g white wine)')
	except:
		print('Does not recognize the type of wine, please input (e.g white wine)')

	try:	
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
		elif country.lower() == 'south african' or country.lower() == 'south_african':
			south_african += 1
		elif country.lower() == 'spanish' or country.lower() == 'spain':
			spanish += 1
		else:
			print('Does not recognize the country, please input valid country')
	except:
		print('Does not recognize the country, please input valid country')
	
	attr = [fine_wine, red_wine, rose_wine, white_wine, argentina, australian, chilean, french, italian, new_zealand, portuguese, south_african, spanish]
  
	for i in attr:
		y_predict.append(i)
	y_predict = np.array(y_predict)
	y_predict = y_predict.reshape(1, -1)
	result = logreg.predict(y_predict)
	if result == 1:
		print('This wine will be favourable with customers')
	elif result == 0:
		print('This wine will be unfavoruable with customers')
	else:
		print('unknown...check inputs')
