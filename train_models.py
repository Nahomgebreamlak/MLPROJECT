from turtle import ht
import sklearn
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix 
import pandas as pd
from sklearn.utils import shuffle
import joblib
import matplotlib.pyplot as plt
import numpy as np
from flask import  render_template

def trainmaltifeatue():
        data = pd.read_csv('./dataset/drebin-215-dataset-5560malware-9476-benign.csv')
        data = shuffle(data)
        X = data.drop(["class"], axis=1)
        Y = data["class"]
        train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.2)
        classifier = SVC(kernel="rbf",C=1)
        classifier.fit(train_x, train_y)
        predicted = classifier.predict(test_x)
        report=classification_report(test_y, predicted) 
        
        clsf_report = pd.DataFrame(classification_report(y_true = test_y, y_pred =predicted, output_dict=True)).transpose()
        # # save the model using joblib in to specified folder
        joblib.dump(classifier, "./static/models/multifeaturemodel")
        html = clsf_report.to_html()

        return  html





def trainpermission():
        data = pd.read_csv('./dataset/android_dataset-v1.csv')
        data = shuffle(data)
        X = data.drop(["class"], axis=1)
        Y = data["class"]
        train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.2)
        classifier = SVC(kernel="rbf",C=1)
        classifier.fit(train_x, train_y)
        predicted = classifier.predict(test_x)
        report=classification_report(test_y, predicted) 
        
        clsf_report = pd.DataFrame(classification_report(y_true = test_y, y_pred =predicted, output_dict=True)).transpose()
        
        # # save the model using joblib in to specified folder
        joblib.dump(classifier, "./static/models/permissionmodel")
        html = clsf_report.to_html()

        return html

        
        