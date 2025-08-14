import mysql.connector
import json

# --- Configuration ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "ml_financial"

# --- Fetch financial data for a company ---
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
        print("❌ MySQL Error:", err)
        return None

# --- Generate analysis ---
def generate_pros_cons(data):
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
        pros.append(f"Profit Growth is strong: {data['profit_growth']}%")
    else:
        cons.append(f"Weak Profit Growth: {data['profit_growth']}%")

    if data["sales_growth_10yr"] > 10:
        pros.append(f"Strong 10-Year Sales Growth: {data['sales_growth_10yr']}%")
    else:
        cons.append(f"Low 10-Year Sales Growth: {data['sales_growth_10yr']}%")

    return pros, cons

# --- Update analysis_backup with pros & cons ---
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
            SET pros = %s,
                cons = %s
            WHERE company_id = %s
        """
        cursor.execute(query, (
            json.dumps(pros),
            json.dumps(cons),
            company_id
        ))

        conn.commit()
        print(f"✅ Updated analysis_backup for {company_id}.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("❌ Failed to update analysis_backup:", err)

# --- Main execution ---
if __name__ == "__main__":
    company_id = input("🔍 Enter company symbol (e.g., INFY): ").strip().upper()

    fin_data = fetch_financial_data(company_id)
    if not fin_data:
        print("❌ No financial data found for:", company_id)
    else:
        pros, cons = generate_pros_cons(fin_data)

        print("\n✅ Pros:")
        for p in pros:
            print(" -", p)

        print("\n⚠️ Cons:")
        for c in cons:
            print(" -", c)

        update_analysis_backup(company_id, pros, cons)
