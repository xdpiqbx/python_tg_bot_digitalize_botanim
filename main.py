import os

import messages_texts
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from books import get_all_books

load_dotenv()


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        update.effective_chat.id,
        messages_texts.GREETINGS
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        update.effective_chat.id,
        messages_texts.HELP
    )


async def all_books_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    all_books_chunks = await get_all_books(chunk_size=60)
    for chunk in all_books_chunks:
        response = "\n".join([book.name for book in chunk])
        await context.bot.send_message(
            update.effective_chat.id,
            text=response
        )


def main() -> None:
    app = (
        ApplicationBuilder()
        .token(os.environ['BOT_API_TOKEN'])
        .build()
    )

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("all_books", all_books_cmd))

    app.run_polling()


if __name__ == "__main__":
    main()
