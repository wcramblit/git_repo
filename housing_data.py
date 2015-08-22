# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:35:34 2015

@author: wcramblit
"""

'''
Instructions:
Analyze sales using regression with any predictors you feel are relevant and justify why regression was appropriate to use

Visualize the coefficients and fitted model

Predict the neighborhood using a k-NN classifier; be sure to withhold a subset of the data for testing. find the variables and k that give you the lowest error

Report and visualize your findings

Describe and decisions that could be made or actions that could be taken from this analysis

'''
import pandas as pd
import pandas as pd
from collections import Counter
import datetime
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt 
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier


df = pd.read_excel('http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_manhattan.xls', sheetname='Manhattan', skiprows=4)

#examine the data set
#start by reviewing values and distributions of neighborhoods, building classes, tax classes, etc.

del df['BOROUGH'] #all values are equal
del df['EASE-MENT'] #all empty values
df['SALE DATE'] = pd.to_datetime(df['SALE DATE']) #convert sale date to datetime
df['PRICELOG'] = np.log(df['SALE PRICE']) #add log sales
df['SALEYEAR'] = df['SALE DATE'].dt.year #convert sale date into year
df['SALEYEAR'] = df['SALEYEAR'].astype(float) #convert to float so it can be correlated properly
df['BLDG_AGE'] = df['SALEYEAR']-df['YEAR BUILT'].astype(float) # conversion to fit in correlation table
df = df[df['SALE PRICE'] != 0] #remove rows with no sale price
df = df[df['ZIP CODE'] != 0] #remove zip codes with 0 values
df.rename(columns=lambda x: x.replace(" ", "_"), inplace=True)#update column headers to make them easier to work with

#create numerical df to make plotting easier
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numeric_df = df.select_dtypes(include=numerics)

# plot each relationship vs. pricelog individually
for k,v in numeric_df.iteritems():
    plt.scatter(df['PRICELOG'], df[k])
    plt.xlabel('PRICELOG')
    plt.ylabel(v)
    plt.show()

#Based on visual inspection, hyperbolic relationship between pricelog and total units, gross square feet. Also, naturally occurring clusters based on zip code; can't be regressed into, but will likely be the main factor in knn analysis

for k, v in numeric_df.iteritems():
    y = np.matrix(df['PRICELOG']).transpose()
    x = np.matrix(df[k]).transpose()
    X = sm.add_constant(x)
    model1 = sm.OLS(y,X).fit()
    print k + " vs. PRICELOG"     
    print 'P vals: ', model1.pvalues
    print 'RSQ', model1.rsquared
    print "\n"

#this analysis tells me we care about building age

#let's try combinations with building age
for k, v in numeric_df.iteritems():
    statement = 'PRICELOG ~ BLDG_AGE + ' + k
    print statement
    model2 = smf.ols(formula=str(statement), data=numeric_df).fit()
    print 'P vals: ', model2.pvalues
    print 'RSQ', model2.rsquared
    print "\n" 
    
    #this identifies "TOTAL UNITS" as marginally improving the model

for k, v in numeric_df.iteritems():
    statement = 'PRICELOG ~ BLDG_AGE * ' + k
    print statement
    model3 = smf.ols(formula=str(statement), data=numeric_df).fit()
    print 'P vals: ', model3.pvalues
    print 'RSQ: ', model3.rsquared
    print "\n" 
    
    #this identifies tax class as an improvement to the model through interaction with age- but I believe it's an overfit. After runnning knn, confirmed that it does not work correctly. Vsually, Zip Code is likely the strongest additional predictor, so going to use Zip, Price, Age.


#KNN analysis
# basis of model: Log of price, Age, Zip predicts neighborhood

'''
1. establish data set with core values
2. create holdout data set
3. Perform knn using a range of k values
4. determine strongest evaluation k distance
5. create model that takes input on age, tax class, price and used knn to predict neighborhood


'''
knn_df = pd.concat([df['BLDG_AGE'], df['PRICELOG'], df['ZIP_CODE'], df['NEIGHBORHOOD'].str.strip()], axis=1)
dfTrain, dfTest = train_test_split(knn_df, test_size=0.2)

result = []
for k in range(1,100):
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(dfTrain[['BLDG_AGE','PRICELOG','ZIP_CODE']],dfTrain['NEIGHBORHOOD'])
    expected = dfTest['NEIGHBORHOOD']
    predicted = knn_model.predict(dfTest[['BLDG_AGE','PRICELOG','ZIP_CODE']])
    error_rate = (predicted != expected).mean()
    print('%d:, %.2f' % (k, error_rate))
    results.append([k, error_rate])
    
result = pd.DataFrame(results, columns=['k', 'error'])

plt.plot(result['k'], results['error'])
plt.xlabel("k-values")
plt.ylabel("Error Rate")
    
#results were terrible with age, price and tax class, but testing with Zip Code made them a hell of a lot better...
    

result = pd.DataFrame(results, columns=['k', 'error'])

plt.plot(result)
plt.xlabel("k-values")
plt.ylabel("Error Rate")
plt.show()
