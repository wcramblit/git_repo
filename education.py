'''
Changes:
Updated comments
Updated line wraps
Updated variable names



'''

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import sqlite3 as lite
import csv
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

# Initiate web scraper.
url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
r= requests.get(url)
soup = BeautifulSoup(r.content)

# Zoom into table.
table = soup('table')[6]
table.find_all('tr')
table = table.tr

# Create a list of the rows.
data = []
for row in table.find_all('tr'):
    data.append(row)

# Remove garbage headers.
del data[0:6]

# Runs a list comp that cleans these up, removing all unicode and key characters found within the table and assigns to a list of lists.
list_of_lists = [[col.string for col in row.find_all("td") if col.string not in {None, u"\xa0", u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h"}] for row in data]

# Remove last few lines of garbage within the table.
del list_of_lists[-11:]

# Pop the headers.
headers = list_of_lists.pop(0)

# Move to a data frame.
df = pd.DataFrame(list_of_lists, columns = headers)
df[['Men','Women','Year','Total']] = df[['Men','Women','Year','Total']].astype(int)

# Ceate a db for this project- let's call it education.db.
con = lite.connect('education.db')
cur = con.cursor()

# Create a table within this db that stores the country name, male, female, and year of analysis.
with con:
	cur.execute("DROP TABLE IF EXISTS UN_data")
	cur.execute('CREATE TABLE UN_data ( country TEXT, male INT, female INT, year INT);')

# Iterate over our data frame by rows to populate our table.
with con:
	for index, row in df.iterrows():
		cur.execute("INSERT INTO UN_data (country, male, female, year) VALUES (?,?,?,?)", (row['Country or area'], row['Men'], row['Women'], row['Year']))


# Start table for data retrieved from GDP spreadsheet.
with con:
	cur.execute("DROP TABLE IF EXISTS gdp")
	con.execute ('CREATE TABLE gdp (country_name TEXT, _1999 INT, _2000 INT, _2001 INT, _2002 INT, _2003 INT, _2004 INT, _2005 INT, _2006 INT, _2007 INT, _2008 INT, _2009 INT, _2010 INT)')

# Read the file and insert it into the table.
with open('ny.gdp.csv','rU') as inputFile:
    next(inputFile)
    next(inputFile)
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        with con:
            cur.execute('INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES ("' + line[0] + '","' + '","'.join(line[43:-5]) + '");')

# Define a data frame from our database
with con:
	cur = con.cursor()
	cur.execute("SELECT * FROM gdp")
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df2 = pd.DataFrame(rows,columns=cols)

con.close()

# Joins our original dataframe containing scraped data with our second dataframe containing data from CSV.
df3 = df.merge(df2, how = 'inner', left_on = 'Country or area', right_on = 'country_name')
del df3['country_name']

# Fix the underscores and replace the column headers so that they can be cross referenced to their corresponding rows.
col_values = df3.columns.values
new_col_values = map(lambda x: x.strip("_"), col_values)
col_val_nums = map(lambda x: int(x), new_col_values[5:])
del new_col_values[5:]
new_col_values = new_col_values + col_val_nums
# Assign the new column names
df3.columns = new_col_values

# Reaassign "country" as index of our new df
df3.set_index(df3["Country or area"], inplace=True)
del df3['Country or area']

# Creates a dictionary that determines the GDP corresponding to the year that our data was taken.
year_GDP = {}
for k, v in df3.iterrows():
    for k2,v2, in df3.iteritems():
        if type(k2) == int and k2 == v["Year"]:
            selection = df3.loc[k,k2]
            if selection != "":
                year_GDP.update({k: selection})

# Convert year_GDP into a DF.
final_vals = pd.DataFrame(year_GDP.items(), columns=['Country', "GDP"])
final_vals.set_index(final_vals['Country'],inplace=True)
del final_vals['Country']

# Merge our new final_vals DF with DF# and drop yearly data to create a final DF4, which contains country, year, men, women and GDP for that year.
df4 = df3.merge(final_vals, how = 'inner', left_index = True, right_index = True)
for num in range(1999, 2011):
    del df4[num]

# For good measure, I'll commit this df to our db. I suspect we could have done the table creation and data selection through SQL but I could not find a solution. Some kind of select from db where year = column name?
con = lite.connect('education.db')
cur = con.cursor()

with con:
	cur.execute("DROP TABLE IF EXISTS value_summary")
	con.execute ('CREATE TABLE value_summary (Country TEXT, Year REAL, Total INT, Men INT, Women INT, GDP INT)')

with con:
	for index, row in df4.iterrows():
		cur.execute("INSERT INTO value_summary (Country, Year, Total, Men, Women, GDP) VALUES (?,?,?,?,?,?)", (index, row['Year'], row['Total'], row['Men'], row['Women'], row['GDP']))

con.close()

# In order to run models, we need to convert our GDPs to their log values to balance the scale
df4['GDPLog'] = np.log(df4['GDP'])

# After running a scatter matrix, it looks like men, women and total all tend toward increase as GDPLog increases

# Run a linear regression.
X = df4['Total']
y = df4['GDPLog']
X = sm.add_constant(X)

model = sm.OLS(y,X).fit()
print model.summary()

# When run for men vs women, men's education has a stronger connection to GDP than women.



