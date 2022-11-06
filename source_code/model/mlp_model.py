import os
#tensorflow
import tensorflow as tf
from tensorflow import keras
#Sklearn 
import sklearn
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn import preprocessing as preproces
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
#arrays and data extractors
import numpy as np
import pandas as pd

#plotting
import matplotlib as mpl
import matplotlib.pyplot as plt

#models
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV
#Seed
np.random.seed(42)
tf.random.set_seed(42)

class MLHelper:   
    @staticmethod
    def AccuracyPrediction(predictions, y_test, classifierName = 'classifier'):
        TP = ((predictions == 1) & (y_test == 1)).sum()
        FP = ((predictions == 1) & (y_test == 0)).sum()
        TN = ((predictions == 0) & (y_test == 0)).sum()
        FN = ((predictions == 0) & (y_test == 1)).sum()
        #accuracy is called precision for classifiers
        # precision = TP/(TP + FP) for true
        # precision = FN/(TN + FN) for false
        print(f'{classifierName} TP:{TP}, FP:{FP}, TN:{TN}, FN:{FN}')

        if((FN == 0 and FP == 0) or (TN == 0 and FN == 0)):
            return

        #percent Fire correctly predicted (on test set)
        precisionForFire = TP/(TP + FP)
        print(f'{classifierName} accuracy for Fire', precisionForFire)
        #percent NoFire correctly predicted (on test set)
        precisionForNoFire = TN/(TN + FN)
        print(f'{classifierName} accuracy for NoFire', precisionForNoFire)
        accuracyOverall = accuracy_score(y_test, predictions)
        print(f'{classifierName} accuracy', accuracyOverall)

# Need to normalize the data between 0 and 1???
# raw data layout
#0 grid_id (0 - 67) 1 degree by 1 degree grids
#1 date (2013-1-1 to 2022-9-30)  - Changed date to be days from start
#2 Reference ETo   (in)   (mm)       
#3 Precipitation   (in)   (mm)      
#4 Solar Radiation Average   (Ly/day)   (W/m²)
#5 Average Vapor Pressure   (mBars)   (kPa)
#6 Maximum Air Temperature   (°F)   (°C)
#7 Minimum Air Temperature   (°F)   (°C)
#8 Average Air Temperature   (°F)   (°C)
#9 Maximum Relative Humidity   (%)
#10 Minimum Relative Humidity   (%)
#11 Average Relative Humidity   (%)
#12 Dew Point   (°F)   (°C)
#13 Average Wind Speed   (mph)   (m/s)
#14 Wind Run   (miles)   (km)
#15 Average Soil Temperature   (°F)   (°C)
#16 has_fire (binary {1:0})

training_data_path = 'D:\\MastersAI\\Stevens\\AppliedMachineLearning\\CPE_695WS\\FinalProject\\mainBranch\\wildfire\\data\\training\\spatial_train_data.csv'

#grid_id,date,eto,precipitation,solar_rad,aver_vapor_press,max_air_temp,min_air_temp,aver_air_temp,max_humidity,min_humidity,aver_humidity,dew_point,aver_wind_speed,wind_run,soil_temp,has_fire
data = pd.read_csv(training_data_path, header=0, delimiter=',')


features = data.drop('has_fire', axis=1)
labels = data['has_fire']

output = labels.to_numpy()

print(f'sum:{np.sum(output)}, max:{np.max(output)}, percentage with fire:{(np.sum(output)/len(output))*100}%')


# Split Data with Pandas Data Frames or can use either numpy.Array
# 80 percent for Training
# 20 percent for Testing

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.8, random_state=42)

# X_train_full, X_test, y_train_full, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

# X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, random_state=42)

scaler = StandardScaler()

#preprocess the data, everything needs to be between 0 and 1
# Y is already between 0 and 1
# X_train_pre = preproces.normalize(X_train.copy())
# X_test_pre = preproces.normalize(X_test.copy())
# X_valid_pre = preproces.normalize(X_valid.copy())

X_train = scaler.fit_transform(X_train)
#X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)

#==============================================
# ExtraTreesClassifier
#==============================================

extra_trees_clf = ExtraTreesClassifier(n_estimators=100, random_state=42, max_depth = 40 ,max_leaf_nodes=40, n_jobs = 4 )
extra_trees_clf.fit(X_train, y_train)
predictions = extra_trees_clf.predict(X_test)

MLHelper.AccuracyPrediction(predictions, y_test, 'ExtraTreesClassifier')

print(f'Feature Importance of ExtraTreesClassifier: {extra_trees_clf.feature_importances_}')


#==============================================
# MLPClassifier using Logistic, Relu, and Tanh activation functions
#==============================================

mlp_clf = MLPClassifier(random_state=42, max_iter=1000, activation = 'logistic', learning_rate = 'constant', momentum = 0.9, solver = 'adam' )
mlp_clf.fit(X_train, y_train)
predictions = mlp_clf.predict(X_test)

MLHelper.AccuracyPrediction(predictions, y_test, 'MLPClassifier_logistic')
print(classification_report(y_test, predictions))

mlp_clf_relu = MLPClassifier(random_state=42, max_iter=1000, activation = 'relu', learning_rate = 'constant', momentum = 0.9, solver = 'adam' )
mlp_clf_relu.fit(X_train, y_train)
predictions = mlp_clf_relu.predict(X_test)

MLHelper.AccuracyPrediction(predictions, y_test, 'MLPClassifier_relu')
print(classification_report(y_test, predictions))

mlp_clf_tanh = MLPClassifier(random_state=42, max_iter=1000, activation = 'tanh', learning_rate = 'constant', momentum = 0.9, solver = 'adam' )
mlp_clf_tanh.fit(X_train, y_train)
predictions = mlp_clf_tanh.predict(X_test)

MLHelper.AccuracyPrediction(predictions, y_test, 'MLPClassifier_tanh')
print(classification_report(y_test, predictions))

#Score all the estimators used and compare
estimators = [mlp_clf, extra_trees_clf, mlp_clf_relu, mlp_clf_tanh]
print('MLPClassifier_logistic', 'ExtraTreesClassifier', 'MLPClassifier_Relu', 'MLPClassifier_tanh')
print([estimator.score(X_test, y_test) for estimator in estimators])

fig = plot_confusion_matrix(mlp_clf, X_test, y_test, display_labels=mlp_clf.classes_)
fig.figure_.suptitle("Confusion Matrix for Fire Spatial Dataset MLPClassifier Logistic")
plt.show()

fig = plot_confusion_matrix(mlp_clf_relu, X_test, y_test, display_labels=mlp_clf_relu.classes_)
fig.figure_.suptitle("Confusion Matrix for Fire Spatial Dataset MLPClassifier Relu")
plt.show()

fig = plot_confusion_matrix(mlp_clf_tanh, X_test, y_test, display_labels=mlp_clf_tanh.classes_)
fig.figure_.suptitle("Confusion Matrix for Fire Spatial Dataset MLPClassifier Tanh")
plt.show()


plt.plot(mlp_clf.loss_curve_)
plt.title("Loss Curve Logistic", fontsize=14)
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.show()

plt.plot(mlp_clf_relu.loss_curve_)
plt.title("Loss Curve Relu", fontsize=14)
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.show()

plt.plot(mlp_clf_tanh.loss_curve_)
plt.title("Loss Curve Tanh", fontsize=14)
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.show()

#hyper tuning
param_grid = {
    'hidden_layer_sizes': [(200,100,50), (50,25,15), (150,75,30)],
    'max_iter': [100, 200, 300],
    'activation': ['tanh', 'relu', 'logistic'],
    'solver': ['sgd', 'adam'],
    'alpha': [0.0001, 0.05],
    'learning_rate': ['constant','adaptive'],
}

#==============================================
# GridSearchCV Hypertuning
#==============================================
# grid = GridSearchCV(mlp_clf, param_grid, n_jobs= -1, cv=5)
# grid.fit(X_train, y_train)
# print(grid.best_params_)

life = 42