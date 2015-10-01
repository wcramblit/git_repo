# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:08:55 2015

@author: wcramblit
"""

import pandas as pd
import numpy as np
import sklearn.datasets as datasets
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.lda import LDA
import sklearn.neighbors as skl


iris = datasets.load_iris()

X = iris.data
y = iris.target
target_names = iris.target_names

pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)

lda = LDA(n_components=2)
X_r2 = lda.fit(X, y).transform(X)

# Percentage of variance explained for each components
print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))

# Plot PCA of sample
plt.figure()
for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
    plt.scatter(X_r[y == i, 0], X_r[y == i, 1], c=c, label=target_name)
plt.legend()
plt.title('PCA of IRIS dataset')

# Plot LDA of sample
plt.figure()
for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
    plt.scatter(X_r2[y == i, 0], X_r2[y == i, 1], c=c, label=target_name)
plt.legend()
plt.title('LDA of IRIS dataset')

plt.show()

import sklearn.neighbors as skl
knn = skl.KNeighborsClassifier(n_neighbors=3)
kneighbor = knn.fit(X_r,y)
print kneighbor.score(X_r,y)
# PCA data returns accuracy of 99.3%

knn2 = skl.KNeighborsClassifier(n_neighbors=3)
kneighbor2 = knn2.fit(X,y)
print kneighbor2.score(X,y)
# Standard data returns accuracy of 96%

knn3 = skl.KNeighborsClassifier(n_neighbors=3)
kneighbor3 = knn3.fit(X_r2,y)
print kneighbor3.score(X_r2,y)
# LDA data returns accuracy of 97%

