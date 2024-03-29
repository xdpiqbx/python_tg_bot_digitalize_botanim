import os

import messages_texts
import config
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from books import (get_all_books,
                   get_already_read_books,
                   get_now_reading_book,
                   get_not_started_books,
                   get_books_by_ids)
from votings import get_actual_voting, save_vote, get_leaders

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


async def vote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await get_actual_voting() is None:
        await context.bot.send_message(
            update.effective_chat.id,
            text=messages_texts.NO_ACTUAL_VOTING,
            parse_mode=constants.ParseMode.HTML
        )
        return
    all_books_by_categories = await get_not_started_books()
    for category in all_books_by_categories:
        books_in_category = "\n".join([f"🆔 [<b>{book.id}</b>] 📙{book.name}" for book in category.books])
        response = f"<b>📚{category.name}</b>:\n\n{books_in_category}"
        await context.bot.send_message(
            update.effective_chat.id,
            text=response,
            parse_mode=constants.ParseMode.HTML
        )
    await context.bot.send_message(
        update.effective_chat.id,
        text=messages_texts.VOTE,
        parse_mode=constants.ParseMode.HTML
    )


async def vote_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await get_actual_voting() is None:
        await context.bot.send_message(
            update.effective_chat.id,
            text=messages_texts.NO_ACTUAL_VOTING,
            parse_mode=constants.ParseMode.HTML
        )
        return
    user_message = update.message.text
    book_ids = [book_id for book_id in user_message.split(' ')]
    if len(set(book_ids)) != config.NUMBER_OF_BOOKS:
        await context.bot.send_message(
            update.effective_chat.id,
            text=messages_texts.VOTE_PROCESS_INCORRECT_INPUT,
            parse_mode=constants.ParseMode.HTML
        )
        return
    books = await get_books_by_ids(book_ids)
    if len(books) != config.NUMBER_OF_BOOKS:
        await context.bot.send_message(
            update.effective_chat.id,
            text=messages_texts.VOTE_PROCESS_INCORRECT_IDENTIFIERS,
            parse_mode=constants.ParseMode.HTML
        )
        await context.bot.send_photo(
            update.effective_chat.id,
            photo=open('resources/img/yoda.png', 'rb')
        )
        return
    response = "Ты выбрал следующие книги: 📚\n\n"
    response += "\n".join([f"🆔 [<b>{book.id}</b>] 📙{book.name}" for book in books])
    response += "\n\nСохранено."
    await context.bot.send_message(
        update.effective_chat.id,
        text=response,
        parse_mode=constants.ParseMode.HTML
    )
    await save_vote(
        update.message.from_user.id,
        [int(book.id) for book in books]
    )


# Vote Conversation
# 1. /vote
# 2. send message with book ids it must be 3 different books
# 3. get books from db and send to user
# 4. user confirm books

async def voteresults_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    vote_leaders = await get_leaders()
    if vote_leaders is None:
        await context.bot.send_message(
            update.effective_chat.id,
            text=messages_texts.NO_VOTE_RESULTS,
            parse_mode=constants.ParseMode.HTML
        )
        return
    response = (f"Голосование с {vote_leaders.vote_start} по {vote_leaders.vote_finish}\n\n"
                f"Top 5 лидеров на сейчас:\n\n")
    response += '\n'.join(
        [
            f"{i}. {leader.book_name}\n"
            f"С рейтингом: {leader.score}\n"
            for i, leader in enumerate(vote_leaders.leaders, 1)
        ]
    )
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

    app.add_handler(
        CommandHandler(
            "vote",
            vote_cmd,
            filters=filters.User(username=os.environ['MY_USER_NAME'])
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^\d{1,3}+\s+\d{1,3}+\s+\d{1,3}$") & ~filters.COMMAND,  # 3 number in text message.
            vote_process
        )
    )

    app.add_handler(
        CommandHandler(
            "voteresults",
            voteresults_cmd,
            filters=filters.User(username=os.environ['MY_USER_NAME'])
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
