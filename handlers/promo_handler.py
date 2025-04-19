from telegram import Update
from telegram.ext import CallbackContext
from database.models import get_user, update_user
from config import *

def promo_code_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user = get_user(chat_id)

    if not user:
        update.message.reply_text("❌ यूज़र डेटा नहीं मिला।")
        return

    if context.user_data.get("awaiting_promo"):
        code = update.message.text.strip().upper()

        # अगर यूज़र पहले ही यह कोड यूज़ कर चुका है
        if user.get("promo_used") == code:
            update.message.reply_text("❌ आपने ये प्रोमो कोड पहले ही इस्तेमाल किया है।")
            return

        # प्रोमो कोड की वैलिडेशन
        if code == "WELCOME100":
            new_balance = user["balance"] + 10
            update_user(chat_id, {
                "balance": new_balance,
                "promo_used": code
            })
            update.message.reply_text("✅ ₹10 आपके अकाउंट में जोड़ दिए गए हैं प्रोमो कोड से।")
        else:
            update.message.reply_text("❌ गलत प्रोमो कोड।")

        context.user_data.pop("awaiting_promo", None)
