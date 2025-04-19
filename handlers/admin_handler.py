from telegram import Update
from telegram.ext import CallbackContext
from database.models import add_country, add_service
from config import ADMIN_ID

def admin_text(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id != ADMIN_ID:
        return  # Unauthorized access

    action = context.user_data.get("admin_action")
    text = update.message.text.strip()

    if action == "add_country":
        try:
            name, code, cid = [x.strip() for x in text.split(",")]
            add_country(name, code, int(cid))
            update.message.reply_text(f"✅ Country Added:\nName: {name}\nCode: {code}\nID: {cid}")
        except:
            update.message.reply_text("❌ Format: India,india,12")

    elif action == "add_service":
        try:
            name, sid, price = [x.strip() for x in text.split(",")]
            add_service(name, sid, int(price))
            update.message.reply_text(f"✅ Service Added: {name} ₹{price}")
        except:
            update.message.reply_text("❌ Format: Telegram,telegram,20")

    context.user_data.pop("admin_action", None)
