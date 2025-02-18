from flask import Flask, jsonify
import pandas as pd 

app = Flask(__name__)

@app.route("/")
def hello_energy():
    return "<p>Let's explore energy companies!</p>"

@app.route("/data", methods=["GET"])
def data_mean():
    df = pd.read_csv("energy.csv")
    intern = df["Total Interns"].mean()
    employee = df["Employees"].mean()
    return jsonify(
        {"The mean of interns": intern},
        {"The mean of employees": employee}
    )

if __name__ == "__main__":
    app.run(debug=True)