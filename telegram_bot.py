from dict import dictionary_data
import logging
from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from dict import dictionary_data
load_dotenv()
# Replace with your own token
TOKEN = os.environ.get("ALAZAR_BOT_TOKEN")



# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def is_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is a member of the channel."""
    try:
        chat_member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)

        # Check if the user is a member, administrator, or owner of the channel
        if chat_member.status in ["member", "administrator", "creator"]:
            logging.info(f"✅ User {user_id} is a member of {CHANNEL_USERNAME}.")
            return True
        else:
            logging.info(f"❌ User {user_id} is NOT a member of {CHANNEL_USERNAME}.")
            return False
    except Exception as e:
        logging.error(f"⚠ Error checking subscription status for user {user_id}: {e}")
        return False  # If error occurs, assume user is not subscribed

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command and checks subscription."""
    user_id = update.message.from_user.id
    
    if await is_subscribed(user_id, context):
        await update.message.reply_text(
            '✅ እንኳን ደህና መጡ! የፈለጉትን ቃል ይጻፉ።'
        )
    else:
        await update.message.reply_text(
            f"እንኳን ደህና መጡ 🙌። ይህንን ቦት ለመጠቀም በቅድሚያ ቻናላችንን ይቀላቀሉ ዘንድ በትህትና እንጠይቃለን \n👉 [Join Here]({CHANNEL_LINK})\n"
            "",
            parse_mode="Markdown"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user messages and checks subscription before responding."""
    user_id = update.message.from_user.id

    if await is_subscribed(user_id, context):
        word = update.message.text
        definition = dictionary_data.get(word.lower(), "ይቅርታ ለዚህ ቃል ተዛማጅ መልስ አላገኘንም 😔🙏")
        await update.message.reply_text(definition)
    else:
        await update.message.reply_text(
            f"⚠ ይቅርታ! በቅድሚያ ቻናላችንን ይቀላቀሉ \n👉 [Join Here]({CHANNEL_LINK})\n"
            "",
            parse_mode="Markdown"
        )


def main() -> None:
    """Main function to run the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()

