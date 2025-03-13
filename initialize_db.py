import duckdb

# initialize the database and populates it with the data from the CSV file.

con = duckdb.connect("energy.db") 

con.sql("""
    CREATE TABLE IF NOT EXISTS energy (
        company_name TEXT,
        total_interns FLOAT,
        employees FLOAT,
        address TEXT,
        town TEXT,
        state TEXT,
        zip TEXT,
        sector TEXT
    )
""")

con.sql("""
    INSERT INTO energy
    SELECT 
        "Company Name", 
        "Total Interns", 
        "Employees", 
        "Address", 
        "Town", 
        "State", 
        "Zip", 
        "Sector"
    FROM read_csv_auto('energy.csv')
""")

con.sql("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        age INTEGER,
        country TEXT
    )
""")

con.sql("""
    INSERT INTO users VALUES 
    ('giulio', 25, 'Italy'), 
    ('naga', 30, 'India')
""")

con.close()