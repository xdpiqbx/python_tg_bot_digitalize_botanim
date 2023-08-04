import os

import messages_texts
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    await context.bot.send_message(
        update.effective_chat.id,
        messages_texts.GREETINGS
    )


def main() -> None:
    app = (
        ApplicationBuilder()
        .token(os.environ['BOT_API_TOKEN'])
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
