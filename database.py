from config import DB_CONFIG
import mysql.connector

def test_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connected to MySQL successfully!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_connection()
