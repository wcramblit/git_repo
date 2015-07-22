#Script prints cities with July as their warmest month

#Open sqlite and pandaas

import sqlite3 as lite
import pandas as pd

#define table content as tuples
cities = (('New York City','NY'),('Boston','MA'),('Chicago','IL'),('Miami','FL'),('Dallas','TX'),('Seattle','WA'),('Portland','OR'),('San Francisco','CA'),('Los Angeles','CA'))
weather = (('New York City', 2013, 'July', 'January', 62),('Boston', 2013, 'July', 'January', 59),('Chicago', 2013, 'July', 'January', 59),('Miami', 2013, 'August', 'January', 84),('Dallas', 2013, 'July', 'January', 77),('Seattle', 2013, 'July', 'January', 61),('Portland', 2013, 'July', 'December', 63),('San Francisco', 2013, 'September', 'December', 64),('Los Angeles', 2013, 'September', 'December', 75))

#connect to the database
con = lite.connect('getting_started.db')

with con:
	cur = con.cursor()

	#create cities and weather tables
	cur.execute("DROP TABLE IF EXISTS cities")
	cur.execute("DROP TABLE IF EXISTS weather")
	cur.execute("CREATE TABLE cities (name text, state text)")
	cur.execute("CREATE TABLE weather(city text, year integer, warm_month text, cold_month text, average_high integer)")

	#insert data into the two tables
	cur.executemany("INSERT INTO cities VALUES(?,?)",cities)
	cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)",weather)

	#join tables and define as a new table; found on stack overflow http://stackoverflow.com/questions/1998770/combine-two-tables-in-sqlite
	#this may be problematic. Other option is to run directly into the pandas dataframe?
	cur.execute("DROP TABLE IF EXISTS joined")
	cur.execute("CREATE TABLE joined (name text, state text, warm_month text)")
	cur.execute("INSERT INTO joined (name, state, warm_month) SELECT cities.name, cities.state, weather.warm_month FROM cities INNER JOIN weather ON name=city")

	#load tables into a pandas dataframe; question about the quotations around July...
	cur.execute("SELECT * FROM joined WHERE warm_month='July' ")
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df = pd.DataFrame(rows, columns=cols)

	#print resulting city and state into a full sentence, for example "the cities that are warmest in July are Las Vegas, NV;..."
	# refer here: http://stackoverflow.com/questions/18012505/python-pandas-dataframe-columns-convert-to-dict-key-and-value
	# I know that this output is improperly done, but I am struggling to figure out how to call dictionary items in a statement
	my_dict = dict(zip(df.name, df.state))
	print "The cities that are hottest in July are: "
	for items in my_dict:
		print items, my_dict[items]

	#Push to Github (external)
