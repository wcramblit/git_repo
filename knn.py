# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 14:55:41 2015

@author: wcramblit
"""

''' 

steps:

1. determine k
2. calculate the distance between new observation and all points in the training set
3. sort the distances to determine the k nearest neighbors based on the k-th minimum distance
4. determine the class of those neighbors
5. determine the majority

'''

import pandas as pd
import numpy as np
import sklearn.datasets as datasets
import matplotlib.pyplot as plt

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

# create scatterplot of sepal length by width in the Iris dataset
'''

NOTE: OMITTED 

x = df['sepal_length']
y = df['sepal_width']
tar = df['target'] #used to assign color based on target value

plt.scatter(x,y,c=tar)
plt.show()
'''

# pick a new point, programmatically at random
test_width = np.random.uniform(min(df['sepal_width']), max(df['sepal_width']))
test_length = np.random.uniform(min(df['sepal_length']), max(df['sepal_length']))

# sort each point by its distance from the new point and subset the 10 nearest points
import math
from scipy import stats

distance_s_length = [i - test_length for i in df['sepal_length']]
distance_s_width = [i - test_width for i in df['sepal_width']]

# calculate euclidean distance for each item
df_dist = pd.DataFrame(data=distance_s_length)
df_dist[1] = distance_s_width
df_dist[2] = map(lambda x,y: math.sqrt((x**2+y**2)),df_dist[0],df_dist[1]) 
df_dist['target'] = df['target']

# sort df_dist by euclidean distance
df_dist.sort([2], inplace=True)

# find majority votes from top 10
votes = df_dist['target']
votes = votes[:10]
category = stats.mode(votes)
print type_dict[category[0].item()]
# will print class of random subset