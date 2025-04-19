import requests
import json
from config import ACCESS_TOKEN, MERCHANT_ID

def verify_utr_with_bharatpay(utr):
    """
    BharatPe API के माध्यम से UTR नंबर को वेरिफाई करता है।
    सफल होने पर True लौटाता है, अन्यथा False।
    """
    try:
        url = "https://api.bharatpe.in/v1/payment/verify"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "utr": utr,
            "merchant_id": MERCHANT_ID
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()

        # status == "PAID" हो तो ही सही माने
        return result.get("status") == "PAID"

    except Exception as e:
        print(f"UTR Verification Error: {e}")
        return False
