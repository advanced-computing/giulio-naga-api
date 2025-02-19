from flask import Flask, jsonify
import pandas as pd 

app = Flask(__name__)

df = pd.read_csv("energy.csv")

@app.route("/")
def hello_energy():
    return "<p>Let's explore energy companies!</p>"

@app.route("/intern")
def intern_mean():
    intern_mean = float(df["Total Interns"].mean())
    intern_min = float(df["Total Interns"].min())
    intern_max = float(df["Total Interns"].max())

    return jsonify(
        {"The mean of interns": intern_mean,
        "The min of interns": intern_min,
        "The max of interns": intern_max}
    )

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

if __name__ == "__main__":
    app.run(debug=True)