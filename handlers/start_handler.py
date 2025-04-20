from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from database.models import get_user, create_user, update_user
from config import ADMIN_ID, SUPPORT_URL, EMOJIS

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.effective_user.first_name
    args = context.args

    # यूज़र डेटा प्राप्त करें या नया यूज़र बनाएं
    user = get_user(chat_id)

    if not user:
        new_user = {
            "_id": chat_id,
            "name": name,
            "balance": 0.0,
            "total_recharged": 0.0,
            "total_numbers": 0,
            "used_numbers": 0,
            "refers": 0,
            "referral_wallet": 0.0,
            "referred_by": None,
            "promo_used": None
        }

        # Referral सिस्टम प्रोसेस करें
        if args:
            try:
                ref_id = int(args[0])
                if ref_id != chat_id:
                    ref_user = get_user(ref_id)
                    if ref_user:
                        new_user["referred_by"] = ref_id
                        update_user(ref_id, {"refers": ref_user.get("refers", 0) + 1})
            except Exception as e:
                print(f"Referral processing error: {e}")

        create_user(chat_id, new_user)
        user = new_user

    # यूज़र को welcome और summary मैसेज भेजें
    msg = (
        f"👋 Hello {user['name']}!\n"
        f"💰 Balance: ₹{user['balance']:.2f}\n"
        f"📦 Total Numbers: {user['total_numbers']}\n"
        f"✅ Used: {user['used_numbers']}"
    )

    # बटन मेन्यू तैयार करें
    buttons = [
        [InlineKeyboardButton(f"{EMOJIS['get_otp']} Get OTP", callback_data="get_otp")],
        [InlineKeyboardButton(f"{EMOJIS['recharge']} Recharge", callback_data="recharge")],
        [InlineKeyboardButton(f"{EMOJIS['profile']} Profile", callback_data="profile")],
        [InlineKeyboardButton(f"{EMOJIS['promo_code']} Promo Code", callback_data="promo_code")],
        [InlineKeyboardButton(f"{EMOJIS['support']} Support", url=SUPPORT_URL)]
    ]

    # एडमिन के लिए एडमिन पैनल का बटन
    if chat_id == ADMIN_ID:
        buttons.append([InlineKeyboardButton(f"{EMOJIS['admin_panel']} Admin Panel", callback_data="admin_panel")])

    update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
