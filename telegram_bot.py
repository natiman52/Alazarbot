from dict import dictionary_data
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
load_dotenv()
# Replace with your own token
TOKEN = os.environ.get("ALAZAR_BOT_TOKEN")

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('እንኳን ደህና መጡ ፣ የፈለጉትን ቃል በመጻፍ ይላኩልኝ ። ሲጽፉ ግን አማርኛ keyboard ይጠቀሙ ።')

def get_definition(word: str) -> str:
    return dictionary_data.get(word.lower(), "ይቅርታ ለዚህ ቃል ተዛማጅ መልስ አላገኘንም 😔🙏")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = update.message.text
    definition = get_definition(word)
    await update.message.reply_text(definition)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()