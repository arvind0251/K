from telegram import Update
from telegram.ext import CallbackContext
from database.models import add_country, add_service, add_promo
from config import ADMIN_ID

def admin_text(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id != ADMIN_ID:
        return

    action = context.user_data.get("admin_action")
    text = update.message.text.strip()

    if action == "add_country":
        try:
            name, cid = [x.strip() for x in text.split(",")]
            add_country(name, int(cid))
            update.message.reply_text(f"✅ Country Added:\nName: {name}\nID: {cid}")
        except:
            update.message.reply_text("❌ Format: India,22")

    elif action == "add_service":
        try:
            name, sid, price = [x.strip() for x in text.split(",")]
            add_service(name, sid, int(price))
            update.message.reply_text(f"✅ Service Added: {name} ₹{price}")
        except:
            update.message.reply_text("❌ Format: Telegram,telegram,20")

    elif action == "add_service_to_country":
        try:
            name, sid, price = [x.strip() for x in text.split(",")]
            cid = context.user_data.get("admin_country_id")
            cname = context.user_data.get("admin_country_name")
            add_service(name, sid, int(price), cid, cname)
            update.message.reply_text(f"✅ Service Added to {cname}: {name} ₹{price}")
        except:
            update.message.reply_text("❌ Format: Name,ID,Price")

    elif action == "add_promo":
        try:
            code, amount = [x.strip() for x in text.split(",")]
            add_promo(code, int(amount))
            update.message.reply_text(f"✅ Promo Added: {code} ₹{amount}")
        except:
            update.message.reply_text("❌ Format: CODE,amount (e.g. WELCOME100,10)")

    context.user_data.pop("admin_action", None)
