from telegram import Update
from telegram.ext import CallbackContext
from database.models import get_user, update_user, get_promo
from config import *

def promo_code_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user = get_user(chat_id)

    if not user:
        update.message.reply_text("❌ यूज़र डेटा नहीं मिला।")
        return

    if context.user_data.get("awaiting_promo"):
        code = update.message.text.strip().upper()

        # Check if user already used this code
        if user.get("promo_used") == code:
            update.message.reply_text("❌ आपने यह प्रोमो कोड पहले ही इस्तेमाल किया है।")
            context.user_data.pop("awaiting_promo", None)
            return

        # Fetch promo from DB
        promo = get_promo(code)
        if not promo:
            update.message.reply_text("❌ गलत या expired प्रोमो कोड।")
        else:
            amount = promo["amount"]
            new_balance = user["balance"] + amount
            update_user(chat_id, {
                "balance": new_balance,
                "promo_used": code
            })
            update.message.reply_text(f"✅ ₹{amount} प्रोमो कोड से जोड़ दिए गए हैं!")

        context.user_data.pop("awaiting_promo", None)
