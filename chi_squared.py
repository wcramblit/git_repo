#write a script called chi_squared.py that loads the data, cleans it
#performs a chi-square test and prints a result

from scipy import stats
import collections
import matplotlib.pyplot as plt 
import pandas as pd

#Load the reduced version of the LC dataset

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#Drop null rows
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])

chi, p = stats.chisquare(freq.values())

print "Chi = " + str(chi)
print "p = " + str(p)