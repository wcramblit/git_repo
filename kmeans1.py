# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 17:55:18 2015

@author: wcramblit
"""

##### SECTION 1 #####

import numpy as np
from scipy.cluster.vq import kmeans
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

df = pd.read_csv('un.csv')
rows = len(df.index) #counts number of rows
nonnull = rows-df.isnull().sum()
# based on this result, anything other than education would be fine for clustering

#determine data types of each column
# df.dtypes
#how many countries are present? Answer- 205

col_names = ['lifeMale','lifeFemale','infantMortality','GDPperCapita']
df2 = pd.DataFrame(df[col_names])
df2.dropna(inplace=True)
k_vals = range(1,11)
k_means = [kmeans(df2.values,k) for k in k_vals]

ssq = [ var for (cent, var) in k_means]

NOTE: Omitted for purposes of continuity
plt.scatter(k_vals, ssq)
plt.xlabel('clusters')
plt.ylabel('ssq')
plt.title('clusters')
plt.show()