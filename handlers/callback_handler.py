from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from database.models import (
    get_user, update_user,
    get_all_countries, get_all_services,
    get_services_by_country_id
)
from utils.otp_service import buy_number_and_wait
from config import QR_CODE_LINK, UPI_ID, ADMIN_ID, SUPPORT_URL

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    query.answer()

    user = get_user(chat_id)
    if not user:
        query.edit_message_text("❌ User not found.")
        return

    data = query.data

    # ---------- USER FUNCTIONS ----------
    if data == "recharge":
        context.user_data["awaiting_utr"] = True
        context.bot.send_photo(chat_id, QR_CODE_LINK,
            caption=f"Pay ₹20 to:\n`{UPI_ID}`\nफिर UTR यहाँ भेजें।", parse_mode="Markdown")

    elif data == "profile":
        msg = f"""👤 {user['name']} | ID: {chat_id}
Balance: ₹{user['balance']}
Used: {user['used_numbers']}
Referral Wallet: ₹{user['referral_wallet']}
Refers: {user['refers']}
Total Recharged: ₹{user['total_recharged']}"""
        query.edit_message_text(msg)

    elif data == "promo_code":
        context.user_data["awaiting_promo"] = True
        query.edit_message_text("Apna promo code bheje:")

    elif data == "get_otp":
        countries = get_all_countries()
        if not countries:
            return query.edit_message_text("❌ कोई देश नहीं जोड़ा गया।")
        buttons = [[InlineKeyboardButton(c['name'], callback_data=f"otp_country_{c['id']}")] for c in countries]
        query.edit_message_text("देश चुनें:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("otp_country_"):
        country_code = data.replace("otp_country_", "")
        context.user_data["otp_country"] = country_code
        services = get_all_services()
        if not services:
            return query.edit_message_text("❌ कोई सर्विस उपलब्ध नहीं है।")
        buttons = [[InlineKeyboardButton(f"{s['name']} (₹{s['price']})", callback_data=f"otp_service_{s['name']}")] for s in services]
        query.edit_message_text("सर्विस चुनें:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("otp_service_"):
        service_name = data.replace("otp_service_", "")
        country_code = context.user_data.get("otp_country")
        services = get_all_services()
        service = next((s for s in services if s['name'] == service_name), None)
        if not service:
            return query.edit_message_text("❌ सर्विस नहीं मिली।")
        price = service["price"]
        if user["balance"] < price:
            return query.edit_message_text(f"❌ ₹{price} बैलेंस चाहिए।")
        update_user(chat_id, {
            "balance": user["balance"] - price,
            "total_numbers": user["total_numbers"] + 1
        })
        query.edit_message_text("🔄 नंबर प्राप्त किया जा रहा है...")
        buy_number_and_wait(context, chat_id, country_code, service["id"], price)

    # ---------- ADMIN PANEL ----------
    elif data == "admin_panel" and chat_id == ADMIN_ID:
        query.edit_message_text("⚙️ Admin Panel", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Country", callback_data="admin_add_country")],
            [InlineKeyboardButton("➕ Add Service", callback_data="admin_add_service")],
            [InlineKeyboardButton("📋 View Services", callback_data="admin_prices")],
            [InlineKeyboardButton("🗺 Manage Services by Country", callback_data="admin_manage_services")],
            [InlineKeyboardButton("🎯 Add Promo Code", callback_data="admin_add_promo")]
        ]))

    elif data == "admin_add_country":
        context.user_data["admin_action"] = "add_country"
        query.edit_message_text("देश भेजें इस फॉर्मेट में:\n`India,22`", parse_mode="Markdown")

    elif data == "admin_add_service":
        context.user_data["admin_action"] = "add_service"
        query.edit_message_text("सर्विस भेजें इस फॉर्मेट में:\n`Telegram,telegram,20`", parse_mode="Markdown")

    elif data == "admin_prices":
        services = get_all_services()
        if not services:
            return query.edit_message_text("कोई सर्विस नहीं जोड़ी गई।")
        lines = [f"{s['name']}: ₹{s['price']} | ID: {s['id']}" for s in services]
        query.edit_message_text("Services:\n" + "\n".join(lines))

    elif data == "admin_manage_services":
        countries = get_all_countries()
        buttons = [[InlineKeyboardButton(c["name"], callback_data=f"admin_country_{c['id']}")] for c in countries]
        query.edit_message_text("किस देश की सर्विस देखनी है?", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("admin_country_"):
        cid = int(data.replace("admin_country_", ""))
        countries = get_all_countries()
        cname = next((c["name"] for c in countries if c["id"] == cid), "Unknown")
        services = get_services_by_country_id(cid)
        lines = [f"📱 {s['name']} | ID: `{s['id']}` | ₹{s['price']}" for s in services]
        context.user_data["admin_country_id"] = cid
        context.user_data["admin_country_name"] = cname
        context.user_data["admin_action"] = "add_service_to_country"
        buttons = [[InlineKeyboardButton("➕ Add Service", callback_data="admin_add_service_to_country")]]
        msg = f"देश: *{cname}*\n\n" + "\n".join(lines or ["⚠️ कोई सर्विस नहीं है।"])
        query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "admin_add_service_to_country":
        query.edit_message_text("सर्विस भेजें इस फॉर्मेट में:\n`Name,ID,Price`", parse_mode="Markdown")

    elif data == "admin_add_promo":
        context.user_data["admin_action"] = "add_promo"
        query.edit_message_text("Promo भेजें इस फॉर्मेट में:\n`CODE,amount`", parse_mode="Markdown")
