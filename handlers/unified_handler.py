from telegram import Update
from telegram.ext import CallbackContext
from handlers.promo_handler import promo_code_handler
from handlers.utr_handler import utr_handler
from handlers.admin_handler import admin_text

def unified_message_handler(update: Update, context: CallbackContext):
    # प्रोमो कोड मोड
    if context.user_data.get("awaiting_promo"):
        return promo_code_handler(update, context)

    # UTR रिचार्ज मोड
    elif context.user_data.get("awaiting_utr"):
        return utr_handler(update, context)

    # एडमिन इनपुट मोड
    elif context.user_data.get("admin_action"):
        return admin_text(update, context)

    # यदि कोई मोड एक्टिव नहीं है
    else:
        update.message.reply_text("❓ कृपया पहले कोई विकल्प चुनें या /start कमांड से शुरू करें।")
