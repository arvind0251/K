import requests
from config import API_KEY

def buy_number_and_wait(context, chat_id, country_code, service_id):
    try:
        url = f"https://5sim.net/v1/user/buy/activation/{country_code}/{service_id}"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        }

        res = requests.get(url, headers=headers)
        data = res.json()

        if res.status_code != 200 or 'id' not in data:
            print("5sim error response:", data)
            context.bot.send_message(chat_id, "❌ नंबर नहीं मिल सका। कृपया बाद में प्रयास करें।")
            return

        phone = data.get("phone")
        context.bot.send_message(chat_id, f"✅ नंबर मिला: {phone}\n⏳ OTP का इंतजार कर रहे हैं...")

        # Optionally: implement polling to fetch SMS using data['id']

    except Exception as e:
        print("buy_number_and_wait error:", e)
        context.bot.send_message(chat_id, "❌ OTP लाने में कुछ समस्या हुई।")
