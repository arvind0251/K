from telegram import Update
from telegram.ext import CallbackContext
from database.models import get_user, update_user
from utils.payment import verify_utr_with_bharatpay
from config import *

def utr_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user = get_user(chat_id)

    if not user:
        update.message.reply_text("❌ यूज़र डेटा नहीं मिला।")
        return

    if context.user_data.get("awaiting_utr"):
        utr = update.message.text.strip()

        if verify_utr_with_bharatpay(utr):
            # ₹20 जोड़ो और referral wallet भी अपडेट करो
            new_balance = user["balance"] + 20
            update_data = {
                "balance": new_balance,
                "total_recharged": user.get("total_recharged", 0) + 20
            }

            # रेफर करने वाले को कमीशन दो
            ref_id = user.get("referred_by")
            if ref_id:
                ref_user = get_user(ref_id)
                if ref_user:
                    ref_wallet = ref_user.get("referral_wallet", 0.0) + 0.6
                    update_user(ref_id, {"referral_wallet": ref_wallet})

            update_user(chat_id, update_data)
            update.message.reply_text("✅ ₹20 रिचार्ज सफल रहा!")
        else:
            update.message.reply_text("❌ UTR वेरिफिकेशन फेल हुआ।")

        context.user_data.pop("awaiting_utr", None)
