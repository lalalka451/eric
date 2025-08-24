import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace with your actual bot token
# WARNING: Do NOT share your token publicly except for this example!
# If this token is compromised, you'll need to revoke it via BotFather.
TOKEN = "7216378599:AAHeIFjv_eX0cLp5tvBbyDoXD79Z5cG624"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the command handler function for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hello {user.mention_html()}! Welcome to your simple bot. Send /start again to see this message.",
        # reply_markup=ForceReply(selective=True), # Optional: if you want to force a reply
    )
    logging.info(f"User {user.id} ({user.first_name}) sent /start")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    logging.info("Bot started. Polling for updates...")
    application.run_polling(poll_interval=3)
    logging.info("Bot stopped.")

if __name__ == "__main__":
    main()