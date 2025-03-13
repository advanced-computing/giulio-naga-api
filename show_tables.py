import duckdb

# Connect to the database
con = duckdb.connect("energy.db")

# Fetch all records from users table
users_df = con.sql("SELECT * FROM users").df()

# Print the users table
if users_df.empty:
    print("No data found in the users table.")
else:
    print("Users table data:")
    print(users_df)

con.close()
