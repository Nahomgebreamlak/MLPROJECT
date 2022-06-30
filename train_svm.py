from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix 
from sklearn.utils import shuffle
import joblib
import pandas as pd

data = pd.read_csv('./Adataset/drebin-215-dataset-5560malware-9476-benign.csv')
data = shuffle(data)
X = data.drop(["class"], axis=1)
Y = data["class"]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
# defining parameter range 
param_grid = {'C': [0.1, 1, 10], 
			'gamma': [1, 0.1, 0.01], 
			'kernel': ['rbf' , 'linear']} 

print("Training started...")
grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3) 

grid.fit(X_train, y_train) 
print("Training completed!")

print(grid.best_params_) 
grid_predictions = grid.predict(X_test) 

# print classification report 
print(classification_report(y_test, grid_predictions)) 
joblib.dump(grid, open('./static/models/testmodel', 'wb'))

