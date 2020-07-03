import logging
import requests
import json

from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hi! Use /doggo to get a doggo pic/video')


def doggo(update, context):
    chat_id = update.message.chat_id
    doggoResponse = json.loads(requests.get(
        'https://random.dog/woof.json').text)
    doggoLink = doggoResponse['url']

    context.bot.send_message(chat_id=chat_id, text=doggoLink)


def doggoJob(context):
    job = context.job
    doggoResponse = json.loads(requests.get(
        'https://random.dog/woof.json').text)
    doggoLink = doggoResponse['url']
    context.bot.send_message(job.context, text=doggoLink)


def doggoEveryday(update, context):
    chat_id = update.message.chat_id
    try:
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_repeating(
            doggoJob, interval=60*60*24, first=0, context=chat_id)
        context.chat_data['job'] = new_job

        update.message.reply_text(
            'I will start sending doggos pics/videos everyday!')
    except (IndexError, ValueError):
        update.message.reply_text('Something went wrong!')


def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("doggo", doggo))
    dp.add_handler(CommandHandler("doggoeveryday", doggoEveryday))
    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
