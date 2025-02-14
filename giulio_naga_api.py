from flask import Flask, jsonify
import pandas as pd 

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/data", methods=["GET"])
def data_mean():
    df = pd.read_csv("energy.csv", encoding='latin1')
    mean_value = df["Total Interns"].mean()
    return jsonify({"The mean of interns": mean_value})

if __name__ == "__main__":
    app.run(debug=True)