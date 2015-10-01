# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:44:57 2015

@author: wcramblit
"""

import sklearn.datasets as datasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import cross_validation


iris = datasets.load_iris()

X = iris.data
y = iris.target
target_names = iris.target_names

train_x, test_x, train_y, test_y = cross_validation.train_test_split(X,y,test_size=0.40,random_state=94)

svc = svm.SVC(kernel='poly')
X = train_x
y = train_y
model = svc.fit(X, y)

print model.score(test_x,test_y)
# scores 91.6%; previous lesson had higher score at 96.7%

# calculate 5-fold cross validation using sklearn k fold
kf = cross_validation.cross_val_score(svc,X,y,cv=5)

print kf.mean()
# mean score is 97%
print np.std(kf)
# std is 2.7%
