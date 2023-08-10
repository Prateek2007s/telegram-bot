import re
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Bot token
TOKEN = '6578215509:AAGqjogNKvJY4M_LyfTWrTb7VVgfkJ75h2c'

# Regular expression pattern to match the desired URLs
url_pattern = r'https://d26g5bnklkwsh4\.cloudfront\.net/.*?/master\.m3u8'

# Function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to URL Uploader Bot! Send me a URL.')

# Function to handle incoming messages
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    urls = re.findall(url_pattern, text)

    context.user_data['urls'] = urls

    update.message.reply_text('Please provide the channel link where you want to upload the lectures.')

    return 'channel_link'

# Function to handle the provided channel link
def handle_channel_link(update: Update, context: CallbackContext):
    channel_link = update.message.text.strip()
    user_urls = context.user_data.get('urls')

    for url in user_urls:
        context.bot.send_message(chat_id=channel_link, text=url)

    update.message.reply_text('Lectures have been uploaded to the specified channel.')

    return ConversationHandler.END

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'channel_link': [MessageHandler(Filters.text & ~Filters.command, handle_channel_link)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
