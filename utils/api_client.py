import requests
from config import API_URL, API_KEY

def get_company_data(company_id):
    try:
        response = requests.get(f"{API_URL}?id={company_id}&api_key={API_KEY}")
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ Error fetching data for {company_id}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    company = "TCS"
    data = get_company_data(company)
    if data:
        print(f"📊 Data for {company}:\n", data)
