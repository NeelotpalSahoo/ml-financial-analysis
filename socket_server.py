import socket
import mysql.connector
import time
import json

# --- DB Configuration ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # 🔐 Enter your actual password if needed
    "database": "ml_financial"
}

# --- Function to get latest analysis data ---
def get_latest_analysis():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT company_id, pros, cons FROM analysis_backup WHERE pros IS NOT NULL AND cons IS NOT NULL")
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # Format and return clean JSON
        return json.dumps(results, indent=2)

    except mysql.connector.Error as err:
        print("❌ MySQL Error:", err)
        return json.dumps({"error": "Database error"})

# --- Start TCP socket server ---
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 9999))
    server_socket.listen(1)

    print("📡 Real-time Analysis Server started on port 9999...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"🔗 Client connected from {addr}")

        try:
            while True:
                analysis_data = get_latest_analysis()
                print("📤 Sending data to client...")

                # Send with newline delimiter
                client_socket.sendall((analysis_data + "\n").encode("utf-8"))
                time.sleep(5)  # Update every 5 seconds

        except (ConnectionResetError, BrokenPipeError):
            print("⚠️ Client disconnected.")
        except Exception as e:
            print("❌ Error during communication:", e)
        finally:
            client_socket.close()

# --- Run the script ---
if __name__ == "__main__":
    start_server()
