import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Halo! Kirimkan file yang ingin Anda ganti namanya dengan mereply file tersebut dengan nama baru.')

def rename_file(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message and update.message.reply_to_message.document:
        file = update.message.reply_to_message.document
        new_name = update.message.text
        file_path = file.get_file().download()
        new_file_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_file_path)
        update.message.reply_document(document=open(new_file_path, 'rb'), filename=new_name)
        os.remove(new_file_path)
    else:
        update.message.reply_text('Silakan reply file yang valid dengan nama baru.')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.reply, rename_file))

    updater.start_polling()
    updater.idle()

@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), updater.bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    main()
