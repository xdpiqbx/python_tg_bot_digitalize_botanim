import os

import messages_texts
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters

from books import get_all_books, get_already_read_books, get_now_reading_book

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
    all_books_by_categories = await get_all_books()
    for category in all_books_by_categories:
        books_in_category = "\n".join([f"{i}. {book.name}" for i, book in enumerate(category.books, 1)])
        response = f"<b>📚{category.name}</b>:\n\n{books_in_category}"
        await context.bot.send_message(
            update.effective_chat.id,
            text=response,
            parse_mode=constants.ParseMode.HTML
        )


async def already_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    books = await get_already_read_books()
    response = "Уже прочитали:\n\n"
    response += '\n'.join([
        f"{i}. {book.name}.\n"
        f"<em>Читали: с {book.read_start.strftime('%d.%m.%Y')} "
        f"по {book.read_finish.strftime('%d.%m.%Y')}</em>"
        for i, book
        in enumerate(books, 1)
    ])
    await context.bot.send_message(
        update.effective_chat.id,
        text=response,
        parse_mode=constants.ParseMode.HTML
    )

async def now_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    books = await get_now_reading_book()
    response = "Сейчас мы читаем 📖:\n\n"
    response += '\n'.join([
        f"{i}. {book.name}.\n"
        f"<em>Читаeм: с {book.read_start.strftime('%d.%m.%Y')}</em>"
        for i, book
        in enumerate(books, 1)
    ])
    await context.bot.send_message(
        update.effective_chat.id,
        text=response,
        parse_mode=constants.ParseMode.HTML
    )


def main() -> None:
    app = (
        ApplicationBuilder()
        .token(os.environ['BOT_API_TOKEN'])
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start_cmd,
            filters=filters.User(username=os.environ['MY_USER_NAME'])
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_cmd,
            filters=filters.User(username=os.environ['MY_USER_NAME'])
        )
    )

    app.add_handler(
        CommandHandler(
            "all_books",
            all_books_cmd,
            filters=filters.User(username=os.environ['MY_USER_NAME'])
        )
    )

    app.add_handler(
        CommandHandler(
            "already",
            already_cmd,
            filters=filters.User(username=os.environ['MY_USER_NAME'])
        )
    )

    app.add_handler(
        CommandHandler(
            "now",
            now_cmd,
            filters=filters.User(username=os.environ['MY_USER_NAME'])
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
