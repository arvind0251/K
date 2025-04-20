import requests
from config import ACCESS_TOKEN, MERCHANT_ID

def verify_utr_with_bharatpay(utr: str) -> int:
    try:
        url = f"https://api.bharatpe.in/v1/transaction/fetch/merchant/{MERCHANT_ID}?txnType=PAYMENT&limit=20"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        # DEBUG: Show what UTR was received and what transactions are fetched
        print("DEBUG UTR (user input):", utr)
        print("Fetched UTRs from BharatPe:")
        for txn in data.get("data", []):
            print("UTR:", txn.get("utr"), "| Amount:", txn.get("amount"))

        # Match and return amount
        for txn in data.get("data", []):
            utr_in_txn = str(txn.get("utr", "")).lower()
            if str(utr).lower() in utr_in_txn:
                return txn.get("amount", 0)

        return 0  # no match found

    except Exception as e:
        print(f"UTR verify error: {e}")
        return 0
