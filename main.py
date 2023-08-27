

import asyncio
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import urllib
from bottoken import TOKEN

debug = os.path.isfile('debug')



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

with open('ids.csv') as ids_file:
    ids = ids_file.read().split(',')

ids = set([int(idd) for idd in ids if idd!=''])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in ids:
        ids.add(chat_id)
        with open('ids.csv', 'w') as ids_file:
            ids_file.write(','.join([str(x) for x in ids]))
    await context.bot.send_message(chat_id=chat_id, text='''/help for more info''')
    await context.bot.send_message(chat_id=chat_id, text="Добро пожаловать. Снова.")

async def resend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id
    photos = update.message.photo
    video = update.message.video
    text=update.message.text
    sticker = update.message.sticker
    for idd in ids:
        if (idd==chat_id)==debug:
            if text is not None:
                await context.bot.send_message(chat_id=idd, text=text)
            elif len(photos):
                await context.bot.send_photo(chat_id=idd, photo=photos[-1])
            elif sticker is not None:
                await context.bot.send_sticker(chat_id=idd, sticker=sticker)
            elif video is not None:
                await context.bot.send_video(chat_id=idd, video=video)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=update.effective_chat.id, text='''
Author: https://t.me/brodyga_45
/help 
/requests
/bags
featurerequest text (without /)
pull request: https://github.com/brodyga45/tg2ch (recommended)
reportbag text (without /)
Avaluable content: text, photo, video, sticker (only one per message)
''')

async def requests1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    frequests = os.listdir('frequests')
    frequests.sort()
    res = 'REQUESTS LIST:\n'
    for idd in frequests:
        with open('frequests/' + str(idd), 'r') as f:
            res += str(idd) + ': ' + f.read() + '\n'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=res)

async def bags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    frequests = os.listdir('bags')
    frequests.sort()
    res = 'BAGS LIST:\n'
    for idd in frequests:
        with open('bags/' + str(idd), 'r') as f:
            res += str(idd) + ': ' + f.read() + '\n'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=res)

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text=update.message.text
    if text[:14]=='featurerequest':
        m = max([int(i) for i in os.listdir('frequests')] + [-1])
        feature_id = m + 1
        with open('frequests/' + str(feature_id), 'w') as frequests_file:
            await context.bot.send_message(chat_id=chat_id, text="Your request has been registered. ID: " + str(m+1))
            frequests_file.write(text)
    elif text[:9]=='reportbag':
        m = max([int(i) for i in os.listdir('bags')] + [-1])
        feature_id = m + 1
        with open('bags/' + str(feature_id), 'w') as frequests_file:
            await context.bot.send_message(chat_id=chat_id, text="Your bug report has been received. ID: " + str(m+1))
            frequests_file.write(text)    


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    feedback_handler = MessageHandler(filters.Regex('^featurerequest.*') | filters.Regex('^reportbag.*'), feedback)
    resend_handler = MessageHandler(~filters.COMMAND, resend)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    requests_handler = CommandHandler('requests', requests1)
    bags_handler = CommandHandler('bags', bags)
    application.add_handler(start_handler)
    application.add_handler(requests_handler)
    application.add_handler(feedback_handler)
    application.add_handler(bags_handler)
    application.add_handler(resend_handler)
    application.add_handler(help_handler)
    application.run_polling()