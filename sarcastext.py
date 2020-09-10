#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from uuid import uuid4
import random 
import configparser
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown

config = configparser.ConfigParser()
config.read('config.ini')
token = config['DEFAULT']['token']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('@sarcastext_bot <TEXT>')


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query

    tmp1 = ""
    tmp2 = ""
    tmp3 = ""

    c = 0
    for i in query:
        if (i.lower() == 'i'):
            tmp1 += 'i'
        elif (i.lower() == 'l'):
            tmp1 += 'L'
        else:
            if (c % 2 == 0):
                tmp1 += i.upper()
            else:
                tmp1 += i.lower()
        c += 1

    c = 0
    for i in query:
        if (i.lower() == 'i'):
            tmp2 += 'i'
        elif (i.lower() == 'l'):
            tmp2 += 'L'            
        else:
            if (c % 2 != 0):
                tmp2 += i.upper()
            else:
                tmp2 += i.lower()
        c += 1   

    c = 0
    for i in query:
        if (i.lower() == 'i'):
            tmp3 += 'i'
        elif (i.lower() == 'l'):
            tmp3 += 'L'            
        else:
            r = random.randint(0, 1) 
            if (r == 0):
                tmp3 += i.upper()
            else:
                tmp3 += i.lower()
        c += 1

         
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Sarcastic 1 : " + tmp1 ,
            input_message_content=InputTextMessageContent(tmp1, parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Sarcastic 2 : " + tmp2,  
            input_message_content=InputTextMessageContent(tmp2, parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Sarcastic 3 : " + tmp3,  
            input_message_content=InputTextMessageContent(tmp3, parse_mode=ParseMode.MARKDOWN))
        ]

    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
