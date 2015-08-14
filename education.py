from bs4 import BeautifulSoup
import requests
import pandas as pd 
import sqlite3 as lite
import csv
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
r= requests.get(url)
soup = BeautifulSoup(r.content)

# zoom into table
table = soup('table')[6]
table.find_all('tr')
table = table.tr

# create a list of the data rows
data = []
for row in table.find_all('tr'):
    data.append(row)

# remove garbage headers
del data[0:6]

# create a loop that cleans these up, assign to a list of lists
list_of_lists = [[col.string for col in row.find_all("td") if col.string not in {None, u"\xa0", u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h"}] for row in data]

#remove last few lines of the table
del list_of_lists[-11:]

#Pop the headers
headers = list_of_lists.pop(0)

# move to a data frame
df = pd.DataFrame(list_of_lists, columns = headers)
df[['Men','Women','Year','Total']] = df[['Men','Women','Year','Total']].astype(int)

#create a db for this project- let's call it education.db
con = lite.connect('education.db')
cur = con.cursor()

#create a table within this db that stores the country name, male, female, and year of analysis
with con:
	cur.execute("DROP TABLE IF EXISTS UN_data")
	cur.execute('CREATE TABLE UN_data ( country TEXT, male INT, female INT, year INT);')

#iterate over our data frame by rows to populate our table
with con:
	for index, row in df.iterrows():
		cur.execute("INSERT INTO UN_data (country, male, female, year) VALUES (?,?,?,?)", (row['Country or area'], row['Men'], row['Women'], row['Year']))


#start table GDP
with con:
	cur.execute("DROP TABLE IF EXISTS gdp")
	con.execute ('CREATE TABLE gdp (country_name TEXT, _1999 INT, _2000 INT, _2001 INT, _2002 INT, _2003 INT, _2004 INT, _2005 INT, _2006 INT, _2007 INT, _2008 INT, _2009 INT, _2010 INT)')

#read file into table
with open('ny.gdp.csv','rU') as inputFile:
    next(inputFile) # skip the first two lines
    next(inputFile)
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        with con:
            cur.execute('INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES ("' + line[0] + '","' + '","'.join(line[43:-5]) + '");')

#Start by defining the second data frame...
with con:
	cur = con.cursor()
	cur.execute("SELECT * FROM gdp")
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df2 = pd.DataFrame(rows,columns=cols)

con.close()

# now I need to find a way to create a join by iterating through row/col
# of df2 to find similar indices in df1

df3 = df.merge(df2, how = 'inner', left_on = 'Country or area', right_on = 'country_name')
del df3['country_name']

#now I need to remove all year values and simplify to only include
#the GDP for the years that we received data from originally

#start by fixing the underscores and replacing the column headers
col_values = df3.columns.values
new_col_values = map(lambda x: x.strip("_"), col_values)
col_val_nums = map(lambda x: int(x), new_col_values[5:])
del new_col_values[5:]
new_col_values = new_col_values + col_val_nums
#Assign new column names
df3.columns = new_col_values

#"Year" column are already ints so now we can cross reference

#Assign "country" as index
df3.set_index(df3["Country or area"], inplace=True)
del df3['Country or area']

#Create a dictionary that determines the GDP corresponding to the
#year that our data was taken
dict = {}
for k, v in df3.iterrows():
    for k2,v2, in df3.iteritems():
        if type(k2) == int and k2 == v["Year"]:
            selection = df3.loc[k,k2]
            #print str(k) + " AND " + str(selection)
            #print selection
            if selection != "":
                dict.update({k: selection})

#convert dict into DF
final_vals = pd.DataFrame(dict.items(), columns=['Country', "GDP"])
final_vals.set_index(final_vals['Country'],inplace=True)
del final_vals['Country']

#merge DFs and drop yearly data
df4 = df3.merge(final_vals, how = 'inner', left_index = True, right_index = True)
for num in range(1999, 2011):
    del df4[num]

#for good measure, let's commit this df to our db
#I suspect we could have done the table creation and data selection
#through SQL but I could not find a solution.
#Some kind of select from db where year = column name?

con = lite.connect('education.db')
cur = con.cursor()

with con:
	cur.execute("DROP TABLE IF EXISTS value_summary")
	con.execute ('CREATE TABLE value_summary (Country TEXT, Year REAL, Total INT, Men INT, Women INT, GDP INT)')

with con:
	for index, row in df4.iterrows():
		cur.execute("INSERT INTO value_summary (Country, Year, Total, Men, Women, GDP) VALUES (?,?,?,?,?,?)", (index, row['Year'], row['Total'], row['Men'], row['Women'], row['GDP']))

con.close()

#next let's run some models
#first, let us start with a plot of the logs of the GDPs
#add a column that has GDPLOG
df4['GDPLog'] = np.log(df4['GDP'])

#ran a scatter matrix...
#looks like men, women and total all tend toward increase as GDPLog increases

#run a linear regression
X = df4['Total']
y = df4['GDPLog']
X = sm.add_constant(X)

model = sm.OLS(y,X).fit()
print model.summary()

#When run for men vs women, men's education has a stronger connection to GDP than women



