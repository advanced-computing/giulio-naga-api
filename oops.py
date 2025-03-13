import oops

# creating a DuckDB database
file = 'data.db'
con = oops.connect(file)

# adding the original data to the database
con.sql(("CREATE OR REPLACE TABLE original_data AS SELECT * FROM original_data"))

# show tables
print(con.sql('SHOW TABLES').fetchdf())

# show the original data
print(con.sql('SELECT * FROM original_data').fetchdf())

# close the connection
con.close()