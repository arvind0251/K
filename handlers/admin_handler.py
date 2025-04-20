from telegram import Update
from telegram.ext import CallbackContext
from database.models import add_country, add_service, add_promo
from config import ADMIN_ID

def admin_text(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text.strip()
    action = context.user_data.get("admin_action")

    if chat_id != ADMIN_ID:
        update.message.reply_text("❌ Unauthorized access.")
        return

    if action == "add_country":
        try:
            name, cid = [x.strip() for x in text.split(",")]
            add_country(name, cid)
            update.message.reply_text(f"✅ Country Added:\nName: {name}\nCode: {cid}")
        except Exception as e:
            print(f"Error in add_country: {e}")
            update.message.reply_text("❌ Format error. सही फॉर्मेट: India,in")

    elif action == "add_service_to_country":
        try:
            name, sid, price = [x.strip() for x in text.split(",")]
            cid = context.user_data.get("admin_country_id")
            cname = context.user_data.get("admin_country_name")
            add_service(name, sid, int(price), cid, cname)
            update.message.reply_text(f"✅ Service added to {cname}: {name} ₹{price}")
        except Exception as e:
            print(f"Error in add_service_to_country: {e}")
            update.message.reply_text("❌ Format error. सही फॉर्मेट: Telegram,telegram,20")

    elif action == "add_promo":
        try:
            code, amount = [x.strip() for x in text.split(",")]
            add_promo(code, int(amount))
            update.message.reply_text(f"✅ Promo added: {code} ₹{amount}")
        except Exception as e:
            print(f"Error in add_promo: {e}")
            update.message.reply_text("❌ Format error. सही फॉर्मेट: WELCOME100,10")

    context.user_data.pop("admin_action", None)
