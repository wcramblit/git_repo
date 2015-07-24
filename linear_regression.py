#NOTE: contains all items from unit, so tons of notes.
#made several print and plot items inactiveimport pandas as pd

import matplotlib.pyplot as plt 
import numpy as np 
import statsmodels.api as sm 

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#start by printing our data to see how it needs to be cleaned
#print loansData['Interest.Rate'][0:5]
#shows that our interest rates have "%"" symbols
#print loansData['Loan.Length'][0:5]
#shows that our loan length has "months"
#print loansData['FICO.Range'][0:5]
#shows that FICO is a range from max to min seperated by "-"

#need to clean up all of these columns using lambdas
#reference this for lambda: http://www.python-course.eu/lambda.php

#Clean interest rates
# NOTE- converting to a float made the percentages into full numbers...
#... Converted to decimal to make sure that the values are true
loansData['Interest.Rate'] = map(lambda x: float(x.rstrip("%"))/100, loansData['Interest.Rate'])
#print "Interest Rate: "
#print loansData['Interest.Rate'][0:5]

#Clean loan length
loansData['Loan.Length'] = map(lambda x: int(x.rstrip(" months")), loansData['Loan.Length'])
#print "Loan Length: "
#print loansData['Loan.Length'][0:5]

#Clean FICO scores
#I did this in a different way. The result is the same because all FICO scores are three numbers...
#... and I can't see the benefit of converting to string then out...
#... is there a better reason that I'm missing?
loansData['FICO.Score'] = map(lambda x: int(x[:3]), loansData['FICO.Range'])
#print "FICO Score: "
#print loansData['FICO.Score'][0:5]

#Plot a histogram of FICO scores
#plt.figure()
#p = loansData['FICO.Score'].hist()
#plt.show()

#Create a scatterplot matrix
# Note to self, it would make more sense to create a matrix of rsquare or pearson values.
# can iterate through the matrix, find values over our threshold...
# then print the relationships that fit the threshold to dig deeper into.
#would be easier to find "meaningful" relationships

#plt.figure()
#a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
#plt.show()

#extract columns
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

# returned as a series- to reshape into "columns" (assume that's what transpose does)

#define dependent variable:
y = np.matrix(intrate).transpose()
#define independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

#create input matrix as x value from independent variables!
x = np.column_stack([x1,x2])

#create linear model

X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()
print f.summary()




