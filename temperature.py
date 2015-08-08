import requests
import sqlite3 as lite
import datetime
import pandas as pd
import numpy as np



cities = {"Austin": '30.303936,-97.754355', "Chicago": '41.837551,-87.681844', "San_Francisco": '37.727239,-123.032229', "Seattle": '47.620499,-122.350876', "Nashville": '36.171800,-86.785002'}
key = '0914e9345f31873188b10c751e0d6f6b/'
url = "https://api.forecast.io/forecast/" + key



end_date = datetime.datetime.now() # by setting this equal to a variable, we fix the calculation to the point when we started the scrip (rather than have things move aroudn while we're coding.)

con = lite.connect('weather.db')
cur = con.cursor()

cities.keys()
with con:
	cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Austin REAL, Chicago REAL, San_Francisco REAL, Seattle REAL, Nashville REAL);')

query_date = end_date - datetime.timedelta(days=30)
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)

#GOOD ABOVE HERE

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day


con.close()

con = lite.connect('weather.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM daily_temp ORDER BY day_of_reading", con ,index_col='day_of_reading')

print "\n"
for k,v in cities.iteritems():
    print str(k) + " mean is: " + str(df[k].mean())
    print str(k) + " median is: " + str(df[k].median())
    print str(k) + " variance is: " + str(np.var(df[k]))
    print str(k) + " fluctuation based on difference between max and min is: " + str(np.amax(df[k])-np.amin(df[k]))
    print "\n"


con.close()


