#!/usr/bin/env python3

import configparser
import logging
import random
import unicodedata
from collections.abc import Callable
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
)

config = configparser.ConfigParser()
config.read("config.ini")
token = config["DEFAULT"]["token"]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
# httpx logs the full request URL (which contains the bot token) at INFO level.
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def sarcasm(text: str, upper: Callable[[int], bool]) -> str:
    """Alternate the case of ``text`` using ``upper(index)`` to decide.

    'i' is always kept lowercase and 'l' always uppercase, since they are
    the most readable that way in the alternating-case ("mocking") style.
    """
    out = []
    for index, char in enumerate(text):
        if char.lower() == "i":
            out.append("i")
        elif char.lower() == "l":
            out.append("L")
        elif upper(index):
            out.append(char.upper())
        else:
            out.append(char.lower())
    return "".join(out)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("@sarcastext_bot <TEXT>")


async def inlinequery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query."""
    # Normalize to NFC so decomposed accents (common on macOS) count as a
    # single character; otherwise combining marks shift the alternation.
    query = unicodedata.normalize("NFC", update.inline_query.query)
    if not query:
        return

    variants = [
        ("Sarcastic 1", sarcasm(query, lambda i: i % 2 == 0)),
        ("Sarcastic 2", sarcasm(query, lambda i: i % 2 != 0)),
        ("Sarcastic 3", sarcasm(query, lambda i: random.randint(0, 1) == 0)),
    ]

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"{label} : {text}",
            input_message_content=InputTextMessageContent(text),
        )
        for label, text in variants
    ]

    await update.inline_query.answer(results)


async def error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    application: Application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(InlineQueryHandler(inlinequery))
    application.add_error_handler(error)

    application.run_polling()


if __name__ == "__main__":
    main()
