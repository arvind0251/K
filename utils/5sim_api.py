import requests
from config import API_KEY

BASE_URL = "https://5sim.net/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

def get_5sim_countries():
    try:
        url = f"{BASE_URL}/guest/countries"
        res = requests.get(url, headers=HEADERS)
        return res.json() if res.status_code == 200 else {}
    except Exception as e:
        print("5sim country fetch error:", e)
        return {}

def get_5sim_services():
    try:
        url = f"{BASE_URL}/guest/products"
        res = requests.get(url, headers=HEADERS)
        return res.json() if res.status_code == 200 else {}
    except Exception as e:
        print("5sim service fetch error:", e)
        return {}
