from handlers.promo_handler import promo_code_handler
from handlers.utr_handler import utr_handler
from handlers.admin_handler import admin_text
from telegram import Update
from telegram.ext import CallbackContext

def unified_message_handler(update: Update, context: CallbackContext):
    # Promo Code Flow
    if context.user_data.get("awaiting_promo"):
        return promo_code_handler(update, context)

    # UTR Recharge Flow
    elif context.user_data.get("awaiting_utr"):
        return utr_handler(update, context)

    # Admin Input Flow
    elif context.user_data.get("admin_action"):
        return admin_text(update, context)

    # Default fallback
    else:
        update.message.reply_text("❓ कृपया पहले कोई विकल्प चुनें। या /start से शुरू करें।")
