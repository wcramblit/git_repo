# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 12:03:19 2015

@author: wcramblit
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot
import sklearn.naive_bayes as nb

df = pd.read_csv('ideal_weight.csv')

# remove single quotes from column names
df.columns = map(lambda x: x.replace("'", ""), df.columns)
# remove single quotes from sex column
df['sex'] = map(lambda x: x.replace("'",""), df['sex'])


'''
Plotting section omitted from program but retained here for records

#plot distribution of ideal vs. actual weight
pyplot.hist(df['ideal'], label='ideal', alpha=0.5) 
# Note that alpha makes the bars transparent
pyplot.hist(df['actual'], label='actual', alpha=0.5)
pyplot.legend(loc='upper right')
pyplot.show()

#plot distributions of difference in weight
pyplot.hist(df['diff'],label='diff')
pyplot.legend(loc='upper right')
pyplot.show()

'''

# map sex to a categorical variable (male = 1, female = 0)

df['sex'] = map(lambda x: 1 if x=='Male' or x==1 else 0, df['sex'])
df
# are there more men or women in the data set?
pd.value_counts(df['sex'])

'''
out:
0    119
1     63

'''

x = df[['actual','ideal','diff']]
y = df['sex']
clf = nb.GaussianNB()
clf.fit(x,y)

print clf.score(x,y) # output accuracy score
'''
out:
0.923076923077
'''

prediction_1 = clf.predict([[145,160,-15]])
prediction_2 = clf.predict([[160,145,15]])

print 'Male' if prediction_1 == 1 else 'Female'
print 'Male' if prediction_2 == 1 else 'Female'

'''
out:
Male
Female
'''
