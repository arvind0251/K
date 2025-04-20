import requests
from config import ACCESS_TOKEN, MERCHANT_ID

def verify_utr_with_bharatpay(utr: str) -> int:
    try:
        # Updated URL with merchantId as a query parameter
        url = f"https://api.bharatpe.in/merchant/v1/transactions?merchantId={MERCHANT_ID}&limit=20"
        
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, timeout=10)

        # DEBUG: Print raw response
        print("FULL API RAW RESPONSE:")
        print(response.text)

        data = response.json()

        # DEBUG: Log user input and fetched UTRs
        print("DEBUG UTR (user input):", utr)
        print("Fetched UTRs from BharatPe:")
        for txn in data.get("data", []):
            print("UTR:", txn.get("utr"), "| Amount:", txn.get("amount"))

        # Try to match the UTR
        for txn in data.get("data", []):
            utr_in_txn = str(txn.get("utr", "")).lower()
            if str(utr).lower() in utr_in_txn:
                return txn.get("amount", 0)

        return 0  # No match found

    except Exception as e:
        print(f"UTR verify error: {e}")
        return 0
