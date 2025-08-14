from sklearn.linear_model import LinearRegression
import numpy as np
import mysql.connector

def predict_sales_growth(company_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ml_financial"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT sales_2019, sales_2020, sales_2021, sales_2022, sales_2023 FROM historical_sales WHERE company_id = %s", (company_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if not row:
        return None
    
    X = np.array([2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)
    y = np.array(row)
    
    model = LinearRegression()
    model.fit(X, y)
    
    predicted_2024 = model.predict([[2024]])[0]
    return round(predicted_2024, 1)
