import pandas as pd 
import duckdb 

#data pull function
def get_latest_data(filename,date):
   year, month, day = date.split('-') 
   year = year[2:]

   data = pd.read_excel(filename)
   col_name = f"PCPI{year}M{month}"
   data = data[['DATE',col_name]]
   return data

# creating a DuckDB database
file = 'data.db'
con = duckdb.connect(file)

# adding the original data to the database
con.sql(("CREATE OR REPLACE TABLE CPI AS SELECT * FROM CPI"))

# show tables
print(con.sql('SHOW TABLES').fetchdf())

# show the original data
print(con.sql('SELECT * FROM CPI').fetchdf())

# close the connection
con.close()