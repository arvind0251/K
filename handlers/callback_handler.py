from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from database.models import get_user, update_user, get_all_countries, get_services_by_country_id
from utils.otp_service import buy_number_and_wait
from config import QR_CODE_LINK, UPI_ID, ADMIN_ID

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    query.answer()

    user = get_user(chat_id)
    if not user:
        query.edit_message_text("❌ User not found.")
        return

    data = query.data

    if data == "get_otp":
        countries = get_all_countries()
        if not countries:
            return query.edit_message_text("❌ कोई देश नहीं जोड़ा गया।")
        buttons = [[InlineKeyboardButton(c["name"], callback_data=f"otp_country_{c['id']}")] for c in countries]
        query.edit_message_text("देश चुनें:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("otp_country_"):
        country_code = data.replace("otp_country_", "")
        context.user_data["otp_country"] = country_code
        services = get_services_by_country_id(country_code)
        if not services:
            return query.edit_message_text("❌ कोई सर्विस उपलब्ध नहीं है।")
        buttons = [[InlineKeyboardButton(f"{s['name']} (₹{s['price']})", callback_data=f"otp_service_{s['id']}")] for s in services]
        query.edit_message_text("सर्विस चुनें:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("otp_service_"):
        service_id = data.replace("otp_service_", "")
        country_code = context.user_data.get("otp_country")
        services = get_services_by_country_id(country_code)
        service = next((s for s in services if s['id'] == service_id), None)

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
        buy_number_and_wait(context, chat_id, service["country_id"], service["id"])
