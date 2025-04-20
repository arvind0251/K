from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from handlers.start_handler import start
from handlers.callback_handler import button_handler
from handlers.unified_handler import unified_message_handler
from config import BOT_TOKEN

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start, pass_args=True))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, unified_message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
