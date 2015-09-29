# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 20:52:14 2015

@author: wcramblit
"""

import pandas as pd
from scipy.cluster.vq import kmeans2
import numpy as np
import matplotlib.pyplot as plt

#read and clean data
df = pd.read_csv('un.csv')
columns = ['lifeMale','lifeFemale','infantMortality','GDPperCapita']
df2 = pd.DataFrame(df[columns])
df2.dropna(inplace=True)

#create clusters
clusters = kmeans2(df2.values,3)
df2['cluster'] = clusters[1]

#plot
plt.scatter( df2['GDPperCapita'], df2['infantMortality'], c=df2['cluster'])
plt.xlabel('GDPperCapita')
plt.ylabel('infantMortality')
plt.show()

#plot
plt.scatter( df2['GDPperCapita'], df2['lifeMale'], c=df2['cluster'])
plt.xlabel('GDPperCapita')
plt.ylabel('lifeMale')
plt.show()

#plot
plt.scatter( df2['GDPperCapita'], df2['lifeFemale'], c=df2['cluster'], cmap=plt.cm.Paired )
plt.xlabel('GDPperCapita')
plt.ylabel('lifeFemale')
plt.show()