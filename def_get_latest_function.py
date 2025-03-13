import pandas as pd 
import duckdb

#Write a get_latest_data function that accepts a pull_date and returns the latest data available up to that date
#For example, if the pull_date is 2004-01-15, the function should return the data from vintage PCPI04M1

#data pull function
def get_latest_data(filename,date):
   year, month, day = date.split('-') 
   year = year[2:]

   data = pd.read_excel(filename)
   col_name = f"PCPI{year}M{month}"
   data = data[['DATE',col_name]]
   return data