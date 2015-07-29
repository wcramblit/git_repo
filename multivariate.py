import pandas as pd 
import numpy as np 
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

#Load lending club data (chose 2013-2014)

#First read in data skipping the URL data in the first row
df = pd.read_csv('LoanStats3c.csv', header = 1)

#Second eliminate NA data
df.dropna(inplace=True)

#annual_inc is stored, but applied conversion just in case
#int_rate is stored as string with % sign at end- use lambda to trim
#Had issues doing as suggested, e.g. df['int_rate'].map(lambda x: float(x.strip("%"))/100)
df['annual_inc'] = map(lambda x: float(x), df['annual_inc'])
df['int_rate'] = map(lambda x: float(x.strip("%"))/100, df['int_rate'])
df['home_ownership'] = map(lambda x: 0 if x == "RENT" else 1, df['home_ownership'])

#first use annual_inc to model int_rate
#next add home_ownership 

#First define independent and dependent variables, using...
# columns = list(df.columns.values)
# print columns
#... to identify names of columns

X = df['annual_inc']
y = df['int_rate']

#add a constant to the data set
X = sm.add_constant(X)

#Run Least Squares model
model = sm.OLS(y,X).fit()
print "Model 1 results, int_rate ~ annual_inc:"
print model.summary()

print '\n'

model2 = smf.ols(formula = 'int_rate ~ annual_inc + home_ownership', data = df).fit()
print "Model 2 results, int_rate ~ annual_inc + home_ownership:"
print model2.summary()

print '\n'

model3 = smf.ols(formula = "int_rate ~ annual_inc * home_ownership", data = df).fit()
print "Model 3 results, int_rate ~ annual_inc * home_ownership:"
print model3.summary()

'''These model results are terrible. I'm not sure if I'm missing something, 
but based on what I'm seeing, income and home ownership are not 
suitable predictors of interest rates''' 