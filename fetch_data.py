import mysql.connector
import json

# --- Database Configuration ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "ml_financial"

# --- Step 1: Fetch all unique company_ids from financial_data ---
def get_all_company_ids():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT company_id FROM financial_data WHERE company_id IS NOT NULL")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        print("❌ Error fetching company IDs:", e)
        return []

# --- Step 2: Fetch data for a specific company_id ---
def fetch_financial_data(company_id):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT roe, dividend_payout, profit_growth, sales_growth_10yr, debt
            FROM financial_data
            WHERE company_id = %s
        """
        cursor.execute(query, (company_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"❌ DB Error for {company_id}:", err)
        return None

# --- Step 3: Analyze data into pros and cons ---
def analyze_financial_data(data):
    pros, cons = [], []

    if data["debt"] <= 0:
        pros.append("Company is almost debt-free.")
    else:
        cons.append(f"High debt: ₹{data['debt']} crore.")

    if data["roe"] > 10:
        pros.append(f"Good Return on Equity (ROE): {data['roe']}%")
    else:
        cons.append(f"Low ROE: {data['roe']}%")

    if data["dividend_payout"] > 10:
        pros.append(f"Healthy Dividend Payout: {data['dividend_payout']}%")
    else:
        cons.append("No significant dividend payout.")

    if data["profit_growth"] > 10:
        pros.append(f"Strong Profit Growth: {data['profit_growth']}%")
    else:
        cons.append(f"Weak Profit Growth: {data['profit_growth']}%")

    if data["sales_growth_10yr"] > 10:
        pros.append(f"Strong 10-Year Sales Growth: {data['sales_growth_10yr']}%")
    else:
        cons.append(f"Low 10-Year Sales Growth: {data['sales_growth_10yr']}%")

    return pros, cons

# --- Step 4: Update analysis_backup table ---
def update_analysis_backup(company_id, pros, cons):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        query = """
            UPDATE analysis_backup
            SET pros = %s, cons = %s
            WHERE company_id = %s
        """
        cursor.execute(query, (
            json.dumps(pros),
            json.dumps(cons),
            company_id
        ))

        conn.commit()
        print(f"✅ Updated analysis for {company_id}.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ Failed to update analysis for {company_id}:", err)

# --- Main runner ---
if __name__ == "__main__":
    company_ids = get_all_company_ids()

    for company_id in company_ids:
        print(f"\n🔍 Processing {company_id}...")
        data = fetch_financial_data(company_id)

        if data:
            pros, cons = analyze_financial_data(data)
            update_analysis_backup(company_id, pros, cons)
        else:
            print(f"⚠️ No data found for {company_id}")
