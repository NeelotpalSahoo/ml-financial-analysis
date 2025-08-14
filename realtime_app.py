from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import mysql.connector
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

conn_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ml_financial"
}

def fetch_and_emit():
    while True:
        conn = mysql.connector.connect(**conn_config)
        cursor = conn.cursor()
        cursor.execute("SELECT company_id, pros, cons FROM analysis_backup")
        data = cursor.fetchall()
        conn.close()

        results = []
        for row in data:
            results.append({
                "company_id": row[0],
                "pros": row[1],
                "cons": row[2]
            })

        socketio.emit("update_analysis", results)
        time.sleep(10)  # Refresh every 10 seconds

@app.route("/")
def index():
    return render_template("realtime.html")

if __name__ == "__main__":
    thread = threading.Thread(target=fetch_and_emit)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True)
