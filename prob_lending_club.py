#Write a script that reads in the loan data, cleans it and loads it to a DF
#generate and save a boxplot, histogram and QQ plot in "Amount.Requested"

import matplotlib.pyplot as plt 
import pandas as pd 
import scipy.stats as stats

ld = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#remove null values
ld.dropna(inplace=True)

#generate a boxplot
ld.boxplot(column = "Amount.Requested")
plt.show()
plt.savefig("requested_boxplot.png")

#generate a histogram
ld.hist(column = "Amount.Requested")
plt.show()
plt.savefig("requested_histogram.png")

#generate a QQ plot
plt.figure()
graph = stats.probplot(ld['Amount.Requested'], dist = "norm",plot = plt)
plt.show()
plt.savefig("requested_QQ.png")