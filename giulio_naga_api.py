from flask import Flask, render_template, jsonify, request, Response
import pandas as pd 
import duckdb

app = Flask(__name__)

df = pd.read_csv("energy.csv")

con = duckdb.connect("file.db")

con.sql("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        age INTEGER,
        country TEXT
        )
""")
con.sql("""
    INSERT INTO users VALUES ("giulio", 25, "Italy"), ("naga", 30, "India");
con.close()

@app.route("/")
def show_table():
    # offset&limit
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=100, type=int)

    query = f"SELECT * FROM energy LIMIT {limit} OFFSET {offset}"
    df = con.sql(query).df()

    return render_template("index.html", table=df.to_html())

@app.route("/intern")
def intern_info():
    query = "SELECT AVG(\"Total Interns\") as mean, MIN(\"Total Interns\") as min, MAX(\"Total Interns\") as max FROM energy"
    result = con.sql(query).df().iloc[0].to_dict()

    return jsonify(
        {"The mean of interns": calculate_intern_mean(df),
        "The min of interns": calculate_intern_min(df),
        "The max of interns": calculate_intern_max(df)}
    )

def calculate_intern_mean(df):
    intern_mean = float(df["Total Interns"].mean())
    return intern_mean

def calculate_intern_min(df):
    intern_min = float(df["Total Interns"].min())
    return intern_min

def calculate_intern_max(df):
    intern_max = float(df["Total Interns"].max())
    return intern_max

@app.route("/employee")
def employee_mean():
    employee_mean = df["Employees"].mean()
    employee_min = df["Employees"].min()
    employee_max = df["Employees"].max()

    return jsonify(
        {"The mean of employees": employee_mean,
        "The min of employees": employee_min,
        "The max of employees": employee_max}
    )

@app.route("/filter_employees", methods=["GET"])
def filter_employees():
    df["Employees"] = pd.to_numeric(df["Employees"], errors="coerce")

    # filter
    filter_employees = request.args.get("a", default=100, type=int)
    filtered_df = df[df["Employees"] >= filter_employees]

    return render_template("index.html", table=filtered_df.to_html())

@app.route("/record/<int:id>", methods=["GET"])
def record(id):
    format_type = request.args.get("format", default="json", type=str).lower()

    if 0 <= id < len(df):
        record = df.iloc[id].to_dict()
        if format_type == "csv":
            csv_data = pd.DataFrame([record]).to_csv(index=False)
            return Response(csv_data, mimetype="text/csv")
        return jsonify(record)
    else:
        return jsonify({"error": "Record not found"}), 404

def compute_employee_stats(df):
    return {
        "The mean of employees": df["Employees"].mean(),
        "The min of employees": df["Employees"].min(),
        "The max of employees": df["Employees"].max(),
    }

if __name__ == "__main__":
    app.run(debug=True)
