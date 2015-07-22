# call pandas
import pandas as pd 
from scipy import stats

#define data string
data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.53, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

#split the string on the newlines
#data.split('\n') would also work
data = data.splitlines()

#use a list comprehension to take a strong and split it into a list to create a list of lists
#see here for information http://www.pythonforbeginners.com/basics/list-comprehensions-in-python
#[EXPRESSION for ITEM in LIST if CONDITIONAL]
data = [i.split(', ') for i in data]

#convert into a pandas data frame
column_names = data[0]
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns=column_names)

#Calculate the mean median and mode of Alcohol and Tobacco

#convert alcohol and tobacco columns o float
df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

#Combine all data into a single df for analysis
df_concat = pd.concat((df['Alcohol'],df['Tobacco']))

#mean
mean = df_concat.mean()
#median
median = df_concat.median()

#Mode... figured out how to handle the error where stats.mode returns a tuple
mode = stats.mode(df_concat)
mode = mode[0].astype(float)

#Range
rng = max(df_concat) - min(df_concat)

#Variance
var = df_concat.var()

#STDev
std = df_concat.std()

print "\n"

print "The mean for the Alcohol and Tobacco dataset is " + str(round(mean,3))
print "The median for the Alcohol and Tobacco dataset is " + str(round(median,3))
print "The mode for the Alcohol and Toacco dataset is " + str(round(mode,3))
print "The range for the Alcohol and Tobacco dataset is " + str(round(rng,3))
print "The variance for the Alcohol and Tobacco dataset is " + str(round(var,3))
print "The standard deviation for the Alcohol and Tobacco dataset is " + str(round(std,3))

print "\n"