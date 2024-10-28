import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Join our discussion on the dedicated channel: https://t.me/minecraft_server_discussion"
    )

async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    server_overview = """
    **Welcome to Our Awesome Server!**
    """
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=server_overview)

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_list = """
    **Server Rules:**

    1. Be polite and friendly!
    2. Don't try to break server in any way, be gentle with it :)
    3. Have fun!
        """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=rules_list)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    available_commands = """
**Welcome to our server bot!**

Available commands:

* /join: Get the link to our discussion channel.
* /explain: Get an overview of our server.
* /rules: View our server rules.
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=available_commands)

def main():
    application = ApplicationBuilder().token('<TOKEN_VALUE>').build()
    
    join_handler = CommandHandler('join', join)
    application.add_handler(join_handler)
    explain_handler = CommandHandler('explain', explain)
    application.add_handler(explain_handler)
    rules_handler = CommandHandler('rules', rules)
    start_handler = CommandHandler('start', start)
    
    application.add_handler(rules_handler)
    application.add_handler(start_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
