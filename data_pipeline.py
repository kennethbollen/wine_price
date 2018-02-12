from data_extract import *
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

steps = [('scaler', StandardScaler()),
         ('knn', KNeighborsClassifier(n_neighbors=6))]

pipeline = Pipeline(steps)

# Specify the hyperparameter space
param_grid = {'n_neighbors':np.arange(1,50)}
# Split into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

# Create a k-NN classifier with 7 neighbors: knn
knn = KNeighborsClassifier(n_neighbors=7)

# Instantiate the GridSearchCV object: cv
knn_cv = GridSearchCV(knn, param_grid, cv=5)

# Fit to the training set
knn_cv.fit(X_train, y_train)
