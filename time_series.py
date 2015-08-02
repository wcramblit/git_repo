import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.api as smf

df = pd.read_csv('LoanStats3b.csv', header=1, low_memory=False)

# converts string to datetime object in pandas:
df['issue_d_format'] = pd.to_datetime(df['issue_d']) 
dfts = df.set_index('issue_d_format') 
#this creates a monthly group with index datetime
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
# this creates the time series for analysis
# is this correct? it seems off as it creates a very short series
loan_count_summary = year_month_summary['issue_d']

#plot moving average
plt.figure()
loan_count_summary.plot(kind = 'bar', label='loan_count')
plt.legend()
plt.show()

#does not appear stationary, but we need more data to determine whether this is stationary.

#plot ACF
smf.graphics.tsa.plot_acf(loan_count_summary)
plt.show()

#plot PACF
smf.graphics.tsa.plot_pacf(loan_count_summary)
plt.show()









