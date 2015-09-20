# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 16:19:38 2015

@author: wcramblit
"""

import numpy as np
import statsmodels.formula.api as smf
import pandas as pd
import sklearn.metrics as skl

# Set seed for reproducible results
np.random.seed(414)

# Gen toy data
X = np.linspace(0, 15, 1000)
y = 3 * np.sin(X) + np.random.normal(1 + X, .2, 1000)

train_X, train_y = X[:700], y[:700]
test_X, test_y = X[700:], y[700:]

train_df = pd.DataFrame({'X': train_X, 'y': train_y})
test_df = pd.DataFrame({'X': test_X, 'y': test_y})

# Linear Fit
poly_linear = smf.ols(formula='y ~ 1 + X', data=train_df).fit()

# Quadratic Fit
poly_quadratic = smf.ols(formula='y ~ 1 + X + I(X**2)', data=train_df).fit()

# using mean squared error as a metric compare the performance of different
# polynomial curves in the training set and in the testing set

linear_intercept = poly_linear.params[0]
linear_coeff = poly_linear.params[1]

quadratic_intercept = poly_quadratic.params[0]
quadratic_x_coeff = poly_quadratic.params[1]
quadratic_i_coeff = poly_quadratic.params[2]

# create an array of predicted values based on fit for test set

linear_preds = []
for i in test_X:
    y = (i * linear_coeff) + linear_intercept
    linear_preds.append(y)
    
quadratic_preds = []
for i in test_X:
    y = (quadratic_i_coeff * i**2) + (quadratic_x_coeff * i) + quadratic_intercept
    quadratic_preds.append(y)
    
# calculate mean squared error of each approach, comparing Y actuals to pred Y values

linear_error = skl.mean_squared_error(test_y, linear_preds)
quadratic_error = skl.mean_squared_error(test_y, quadratic_preds)

print "linear error = " + str(linear_error)
print "quadratic error = " + str(quadratic_error)