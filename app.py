from flask import Flask, render_template
import pandas as pd
import pyodbc

app = Flask(__name__)


def get_sales():
    conn = pyodbc.connect(
        "driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=salesDB;"
        "Trusted_Connection=yes;"
    )
    df = pd.read_sql("select * from sales1", conn)
    conn.close()
    return df


@app.route("/", methods=["GET"])
def dashboard():
    sales_df = get_sales()
    data = sales_df.to_dict(orient="records")
    return render_template("index.html", sales=data)


if __name__ == "__main__":
    app.run(port=5001, debug=True, use_reloader=False)
