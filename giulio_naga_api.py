from flask import Flask, render_template, jsonify, request, Response
import pandas as pd 
import duckdb

app = Flask(__name__)

# df = pd.read_csv("energy.csv")

def get_connection():
    return duckdb.connect("energy.db")  # create a connection to the database

# @app.route("/")
# def show_table():
#     offset = request.args.get("offset", default=0, type=int)
#     limit = request.args.get("limit", default=100, type=int)
#     query = f"SELECT * FROM energy LIMIT {limit} OFFSET {offset}"
#     df = con.sql(query).df()

#     return render_template("index.html", table=df.to_html())

@app.route("/")
def show_table():
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=100, type=int)
    
    con = get_connection()
    query = "SELECT * FROM energy LIMIT ? OFFSET ?"
    df = con.execute(query, [limit, offset]).df()
    con.close()

    return render_template("index.html", table=df.to_html())

# def calculate_intern_mean(df):
#     intern_mean = float(df["Total Interns"].mean())
#     return intern_mean

# def calculate_intern_min(df):
#     intern_min = float(df["Total Interns"].min())
#     return intern_min

# def calculate_intern_max(df):
#     intern_max = float(df["Total Interns"].max())
#     return intern_max

# @app.route("/intern")
# def intern_info():
#     query = """
#         SELECT 
#             CAST(AVG("Total Interns") AS FLOAT) as mean, 
#             CAST(MIN("Total Interns") AS FLOAT) as min, 
#             CAST(MAX("Total Interns") AS FLOAT) as max 
#         FROM energy
#     """
#     result = con.sql(query).df().iloc[0].to_dict()
#     return jsonify(result)

# @app.route("/employee")
# def employee_mean():
#     employee_mean = df["Employees"].mean()
#     employee_min = df["Employees"].min()
#     employee_max = df["Employees"].max()

#     return jsonify(
#         {"The mean of employees": employee_mean,
#         "The min of employees": employee_min,
#         "The max of employees": employee_max}
#     )

@app.route("/employee")
def employee_info():
    con = get_connection()
    query = """
        SELECT AVG(Employees) as mean, 
               MIN(Employees) as min, 
               MAX(Employees) as max 
        FROM energy
    """
    result = con.execute(query).df().iloc[0].to_dict()
    con.close()
    return jsonify(result)

# @app.route("/filter_employees", methods=["GET"])
# def filter_employees():
#     df["Employees"] = pd.to_numeric(df["Employees"], errors="coerce")

#     # filter
#     filter_employees = request.args.get("a", default=100, type=int)
#     filtered_df = df[df["Employees"] >= filter_employees]

#     return render_template("index.html", table=filtered_df.to_html())

@app.route("/filter_employees", methods=["GET"])
def filter_employees():
    filter_value = request.args.get("a", default=100, type=int)
    
    con = get_connection()
    query = "SELECT * FROM energy WHERE Employees >= ?"
    df = con.execute(query, [filter_value]).df()
    con.close()
    
    return render_template("index.html", table=df.to_html())

# @app.route("/record/<int:id>", methods=["GET"])
# def record(id):
#     format_type = request.args.get("format", default="json", type=str).lower()

#     if 0 <= id < len(df):
#         record = df.iloc[id].to_dict()
#         if format_type == "csv":
#             csv_data = pd.DataFrame([record]).to_csv(index=False)
#             return Response(csv_data, mimetype="text/csv")
#         return jsonify(record)
#     else:
#         return jsonify({"error": "Record not found"}), 404

@app.route("/record/<int:id>", methods=["GET"])
def record(id):
    format_type = request.args.get("format", default="json", type=str).lower()
    
    con = get_connection()
    query = "SELECT * FROM energy LIMIT 1 OFFSET ?"
    df = con.execute(query, [id]).df()
    con.close()
    
    if df.empty:
        return jsonify({"error": "Record not found"}), 404

    record = df.iloc[0].to_dict()

    if format_type == "csv":
        csv_data = pd.DataFrame([record]).to_csv(index=False)
        return Response(csv_data, mimetype="text/csv")

    return jsonify(record)

# def compute_employee_stats(df):
#     return {
#         "The mean of employees": df["Employees"].mean(),
#         "The min of employees": df["Employees"].min(),
#         "The max of employees": df["Employees"].max(),
#     }

# @app.route("/add_user", methods=["POST"])
# def add_user():
#     data = request.json 
#     username = data.get("username")
#     age = data.get("age")
#     country = data.get("country")

#     if not username or not age or not country:
#         return jsonify({"error": "Missing required fields"}), 400

#     con.sql("INSERT INTO users VALUES (?, ?, ?)", (username, age, country))

#     return jsonify({"message": "User added successfully"}), 201

@app.route("/add_user", methods=["GET"])
def add_user():
    username = request.args.get("username")
    age = request.args.get("age", type=int)
    country = request.args.get("country")

    if not username or not age or not country:
        return jsonify({"error": "Missing required fields"}), 400
    
    con = get_connection()
    con.execute("INSERT INTO users (username, age, country) VALUES (?, ?, ?)", 
                [username, age, country])
    con.close()

    return jsonify({"message": "User added successfully"}), 201

@app.route("/user_stats", methods=["GET"])
def user_stats():
    con = get_connection()
    total_users = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    avg_age = con.execute("SELECT AVG(age) FROM users").fetchone()[0]
    
    query = """
        SELECT country, COUNT(*) as user_count 
        FROM users 
        GROUP BY country 
        ORDER BY user_count DESC 
        LIMIT 3
    """
    top_countries = con.execute(query).df().to_dict(orient="records")
    con.close()
    
    return jsonify({
        "total_users": total_users,
        "average_age": avg_age,
        "top_countries": top_countries
    })

if __name__ == "__main__":
    app.run(debug=True)