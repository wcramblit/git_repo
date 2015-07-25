import pandas as pd 
import matplotlib.pyplot as plt 
import statsmodels.api as sm 
import numpy as np 

#Read in clean data
df = pd.read_csv('loansData_clean.csv')

# Add TF column
df['IR_TF'] = map(lambda x: 1 if x > 0.12 else 0, df['Interest.Rate'])

#add column with constant intercept of 1.0
df = sm.add_constant(df)

#extract column names of independent variables into list
ind_vars = ["Amount.Requested","FICO.Score","const"]

#run model
logit = sm.Logit(df['IR_TF'], df[ind_vars])
result = logit.fit()
coeff = result.params
print coeff

#coeff is a series, meaning that each value can be called.
#I'd like to use "ind_vars" to build this function in an even more
#automated fashion- user would import clean data, program would
#define ind_vars based on results of a linear regression matrix (or even correlation)
#then use that to define regression and finally feed into the functoin.
#I'm almost certain that that's where we're going, so I'll wait...

def logistic_function(co):
	FICO = input("Enter Fico Score: ")
	loanamt = input("Enter Loan Amount: ")

	p = 1/(1 + np.exp(co["const"] + (co["FICO.Score"] * FICO) - (co["Amount.Requested"] * loanamt)))

	print "p = " + str(p)
	return p

#Predict whether user can have a loan
def pred(p):
	if p >= 0.7:
		print "Congratulations, you may have a loan"
	else:
		print "Sorry, no loans for you"

#calls the function using output of logistic function to send p to pred
pred(logistic_function(coeff))