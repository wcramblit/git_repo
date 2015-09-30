# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 22:19:37 2015

@author: wcramblit
"""

import pandas as pd
import numpy as np
import sklearn.datasets as datasets
import matplotlib.pyplot as plt
from sklearn import svm

iris = (datasets.load_iris())
data_x = iris['data']
data_y = iris['target'] 
cols = ['sepal_length','sepal_width','petal_length','petal_width']
type_dict = {0: "Iris-Setosa",
            1: "Iris-Versicolour",
            2: "Iris-Verginica"
            }

df = pd.DataFrame(data = data_x, columns = cols)
df['target'] = data_y

from matplotlib.colors import ListedColormap
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

def plot_estimator(estimator, X, y):
    estimator.fit(X, y)
    x_min, x_max = X[:, 0].min() - .1, X[:, 0].max() + .1
    y_min, y_max = X[:, 1].min() - .1, X[:, 1].max() + .1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 1000),
                         np.linspace(y_min, y_max, 1000))
    Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
    plt.axis('tight')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# our best support vector is sepal_length vs. petal_width, at X = df.ix[:,[0,2]].values

svc = svm.SVC(kernel='poly')
X = df.ix[:,[0,2]].values
y = data_y
model = svc.fit(X, y)

plot_estimator(svc,X,y)


