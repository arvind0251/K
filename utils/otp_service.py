import requests
import time
import threading
from config import API_KEY
from database.models import get_user, update_user

HEADERS_5SIM = {
    "Authorization": f"Bearer {API_KEY}"
}

def buy_number_and_wait(context, chat_id, country, service_id, price):
    """
    5sim API से नंबर खरीदता है और OTP आने तक वेट करता है।
    अगर OTP मिल गया तो यूज़र को भेजता है,
    नहीं मिला तो ₹ refund कर देता है।
    """

    # Step 1: Buy Number
    url = f"https://5sim.net/v1/user/buy/activation/any/{country}/{service_id}"
    res = requests.get(url, headers=HEADERS_5SIM)

    if res.status_code != 200:
        context.bot.send_message(chat_id, "❌ नंबर नहीं मिल सका। 5sim API error.")
        # ₹ refund (optional)
        user = get_user(chat_id)
        update_user(chat_id, {"balance": user["balance"] + price})
        return

    data = res.json()
    number = data["phone"]
    number_id = data["id"]

    context.bot.send_message(chat_id, f"✅ आपका नंबर है: {number}\nOTP का इंतज़ार किया जा रहा है...")

    # Step 2: Poll for OTP
    def poll_otp():
        for _ in range(1200):  # 20 मिनट तक इंतजार (1200 बार 1 सेकंड का स्लीप)
            check = requests.get(f"https://5sim.net/v1/user/check/{number_id}", headers=HEADERS_5SIM).json()
            sms_list = check.get("sms", [])

            if sms_list:
                otp = sms_list[0]["code"]
                context.bot.send_message(chat_id, f"🔐 OTP मिला: `{otp}`", parse_mode="Markdown")

                # Mark number as finished
                requests.get(f"https://5sim.net/v1/user/finish/{number_id}", headers=HEADERS_5SIM)

                # Update used_numbers
                user = get_user(chat_id)
                update_user(chat_id, {"used_numbers": user["used_numbers"] + 1})
                return

            time.sleep(1)

        # Timeout हुआ – cancel number & refund
        requests.get(f"https://5sim.net/v1/user/cancel/{number_id}", headers=HEADERS_5SIM)
        user = get_user(chat_id)
        update_user(chat_id, {"balance": user["balance"] + price})
        context.bot.send_message(chat_id, "❌ OTP नहीं मिला। ₹ refund कर दिया गया।")

    threading.Thread(target=poll_otp).start()
