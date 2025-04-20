import requests
from config import ACCESS_TOKEN, MERCHANT_ID

def verify_utr_with_bharatpay(utr: str) -> bool:
    try:
        url = f"https://api.bharatpe.in/v1/transaction/fetch/merchant/{MERCHANT_ID}?txnType=PAYMENT&limit=20"

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        for txn in data.get("data", []):
            utr_in_txn = str(txn.get("utr", "")).lower()
            if str(utr).lower() in utr_in_txn:
                return True

        return False

    except Exception as e:
        print(f"UTR verify error: {e}")
        return False
