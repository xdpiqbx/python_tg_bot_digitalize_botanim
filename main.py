import os

import messages_texts
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# from db.database import Database

load_dotenv()

# db = Database()


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    with open('db/init_database.sql', 'r') as sql_file:
        sql_text = sql_file.read()
    sql_queries = sql_text.split(';')


    await context.bot.send_message(
        update.effective_chat.id,
        messages_texts.GREETINGS
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        update.effective_chat.id,
        messages_texts.HELP
    )


def main() -> None:
    app = (
        ApplicationBuilder()
        .token(os.environ['BOT_API_TOKEN'])
        .build()
    )

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    app.run_polling()


if __name__ == "__main__":
    main()
