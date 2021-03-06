import requests
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt 
import pandas as pd
import sqlite3 as lite
import time
from dateutil.parser import parse 
import collections
import schedule

#create tables
r = requests.get('http://www.citibikenyc.com/stations/json')
df = json_normalize(r.json()['stationBeanList'])

con = lite.connect('citi_bike.db')
cur = con.cursor()

with con:
	cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

#a prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#for loop to populate values in the database
with con:
	for station in r.json()['stationBeanList']:
		cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

#create the table
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

##########

#create script that downloads the data, parses the result and uploads
#the data to the database
#The code needs to sleep for a minute and perform the same task
#The code needs to run for an hour


def data_updater():
	for i in range(60):
		r = requests.get('http://www.citibikenyc.com/stations/json')
		exec_time = parse(r.json()['executionTime'])

		cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))
		id_bikes = collections.defaultdict(int)

		for station in r.json()['stationBeanList']:
			id_bikes[station['id']] = station['availableBikes']

		for k, v in id_bikes.iteritems():
			cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
		
		con.commit()

		time.sleep(60)
	con.close()

#how can I make sure that this is working properly?
data_updater()