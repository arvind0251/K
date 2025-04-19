from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from handlers.start_handler import start
from handlers.callback_handler import button_handler
from handlers.promo_handler import promo_code_handler
from handlers.utr_handler import utr_handler
from handlers.admin_handler import admin_text
from config import BOT_TOKEN

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start, pass_args=True))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, promo_code_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, utr_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, admin_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
