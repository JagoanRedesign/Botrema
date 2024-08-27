import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Halo! Kirimkan file yang ingin Anda ganti namanya dengan mereply file tersebut dengan nama baru.')

async def rename_file(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message and update.message.reply_to_message.document:
        file = update.message.reply_to_message.document
        new_name = update.message.text
        file_path = await file.get_file().download()
        new_file_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_file_path)
        await update.message.reply_document(document=open(new_file_path, 'rb'), filename=new_name)
        os.remove(new_file_path)
    else:
        await update.message.reply_text('Silakan reply file yang valid dengan nama baru.')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY, rename_file))

    application.run_polling()

@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return 'ok'

if __name__ == '__main__':
    main()
