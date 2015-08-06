import pandas as pd 
import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()


df1 = pd.read_sql_query("SELECT * FROM available_bikes", con, index_col='execution_time')
df2 = pd.read_sql_query("SELECT * FROM citibike_reference", con, index_col='id')

#print df1.head()
#print df2.head()

print len(df1.index)
print len(df2.index)
