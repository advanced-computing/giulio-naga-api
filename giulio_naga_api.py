from flask import Flask, render_template, jsonify, request, Response
import pandas as pd 

app = Flask(__name__)

df = pd.read_csv("energy.csv")

@app.route("/")
def show_table():
    # offset&limit
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=100, type=int)
    paginated_df = df.iloc[offset: offset + limit]

    return render_template("index.html", table=paginated_df.to_html())

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

if __name__ == "__main__":
    app.run(debug=True)
