from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import mysql.connector
import re
import json
from ml_model import predict_sales_growth
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ml_financial"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT company_id FROM analysis_backup WHERE company_id IS NOT NULL")
        companies = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return render_template('analysis.html', companies=companies)
    except Exception as e:
        print("❌ Error loading companies:", e)
        return render_template('analysis.html', companies=[])
    
@app.route('/predict/<company>')
def predict(company):
    # You can pass company name for logging or future use.
    predicted_growth = predict_sales_growth(years_in_future=1)
    return jsonify({"predicted_growth": predicted_growth})

def extract_metrics(text):
    pattern = r"(TTM|3 Years|5 Years|10 Years|Last Year):\s*([\d.]+%)"
    found = dict(re.findall(pattern, text))
    return {
        "TTM": found.get("TTM", "--"),
        "3Y": found.get("3 Years", "--"),
        "5Y": found.get("5 Years", "--"),
        "10Y": found.get("10 Years", "--"),
        "Last": found.get("Last Year", "--")
    }

@socketio.on("send_data")
def handle_send_data(data):
    company = data.get("company")
    print(f"📨 Received company: {company}")

    if not company:
        emit("analysis_update", {"error": "No company selected."})
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ml_financial"
        )
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                compounded_sales_growth,
                compounded_profit_growth,
                roe,
                pros,
                cons
            FROM analysis_backup
            WHERE company_id = %s
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query, (company,))
        row = cursor.fetchone()
        print("✅ DB Row:", row)

        if not row:
            emit("analysis_update", {"error": "No data found for this company."})
            return

        sales = extract_metrics(row["compounded_sales_growth"])
        profit = extract_metrics(row["compounded_profit_growth"])
        roe = extract_metrics(row["roe"])

        pros = [p.strip() for p in row["pros"].split(",")] if row["pros"] else []
        cons = [c.strip() for c in row["cons"].split(",")] if row["cons"] else []

        emit("analysis_update", {
            "sales_growth": sales,
            "profit_growth": profit,
            "roe_growth": roe,
            "pros": pros,
            "cons": cons
        })

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Server Error:", e)
        emit("analysis_update", {"error": "Server error occurred."})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5050)
