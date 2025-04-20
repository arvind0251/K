from telegram import Update
from telegram.ext import CallbackContext
from database.models import get_user, update_user, is_utr_used, mark_utr_as_used
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

        # Step 1: check if UTR is already used
        if is_utr_used(utr):
            update.message.reply_text("⚠️ यह UTR पहले ही इस्तेमाल किया जा चुका है।")
            context.user_data.pop("awaiting_utr", None)
            return

        # Step 2: verify with BharatPe and get actual amount
        amount = verify_utr_with_bharatpay(utr)
        if amount > 0:
            mark_utr_as_used(utr)  # mark it as used now

            # Recharge with actual amount
            new_balance = user["balance"] + amount
            update_data = {
                "balance": new_balance,
                "total_recharged": user.get("total_recharged", 0) + amount
            }

            # Referral reward (optional)
            ref_id = user.get("referred_by")
            if ref_id:
                ref_user = get_user(ref_id)
                if ref_user:
                    ref_wallet = ref_user.get("referral_wallet", 0.0) + 0.6
                    update_user(ref_id, {"referral_wallet": ref_wallet})

            update_user(chat_id, update_data)
            update.message.reply_text(f"✅ ₹{amount} रिचार्ज सफल रहा!")
        else:
            update.message.reply_text("❌ UTR वेरिफिकेशन फेल हुआ या राशि अमान्य है।")

        context.user_data.pop("awaiting_utr", None)
