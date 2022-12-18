import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

data = pandas.read_csv('../../data/training/small_test.csv')
data['eto'].fillna((data['eto'].mean()), inplace=True)
data['precipitation'].fillna((data['precipitation'].mean()), inplace=True)
data['solar_rad'].fillna((data['solar_rad'].mean()), inplace=True)
data['aver_vapor_press'].fillna((data['aver_vapor_press'].mean()), inplace=True)
data['max_air_temp'].fillna((data['max_air_temp'].mean()), inplace=True)
data['min_air_temp'].fillna((data['min_air_temp'].mean()), inplace=True)
data['aver_air_temp'].fillna((data['aver_air_temp'].mean()), inplace=True)
data['max_humidity'].fillna((data['max_humidity'].mean()), inplace=True)
data['min_humidity'].fillna((data['min_humidity'].mean()), inplace=True)
data['aver_humidity'].fillna((data['aver_humidity'].mean()), inplace=True)
data['dew_point'].fillna((data['dew_point'].mean()), inplace=True)
data['aver_wind_speed'].fillna((data['aver_wind_speed'].mean()), inplace=True)
data['wind_run'].fillna((data['wind_run'].mean()), inplace=True)
data['soil_temp'].fillna((data['soil_temp'].mean()), inplace=True)

no_fire = data.loc[data['has_fire']==0]
has_fire = data.loc[data['has_fire']==1]
class_count_0, class_count_1 = data['has_fire'].value_counts()
print(class_count_1, class_count_0)

# go for under sampling
has_fire_over = has_fire.sample(class_count_0, replace=True)
balanced_data = shuffle(pandas.concat([has_fire_over, no_fire]))
train, test = train_test_split(balanced_data, test_size=0.2, random_state=32)

# train_hasfire, test_hasfire = train_test_split(has_fire, test_size=0.2, random_state=32)
# train_nofire, test_nofire = train_test_split(no_fire, test_size=0.2, random_state=32)
# train = shuffle(pandas.concat([train_hasfire, train_nofire]))
# test = shuffle(pandas.concat([test_hasfire, test_nofire]))
#
logisticRegr = LogisticRegression(max_iter=1000)
logisticRegr.fit(train.iloc[:, 3:-1], train.iloc[:, -1])
predictions = logisticRegr.predict(test.iloc[:, 3:-1])
cm = classification_report(test.iloc[:, -1], predictions)
print(cm)

tree = DecisionTreeClassifier(max_depth=10)
tree.fit(train.iloc[:, 3:-1], train.iloc[:, -1])
predictions2 = tree.predict(test.iloc[:, 3:-1])
cm2 = classification_report(test.iloc[:, -1], predictions2)
print(cm2)