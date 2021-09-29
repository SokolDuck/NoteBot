import logging
import os
from dotenv import load_dotenv

load_dotenv()

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import sqlite3
con = sqlite3.connect('example.db', check_same_thread=False)

cur = con.cursor()

def init_db():
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, 'db_init.sql')) as script:
        cur.executescript(script.read())

init_db()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_user_id(update, context):
    user = update.effective_user
    db_user_record = cur.execute(f"SELECT * FROM user WHERE id={user.id}")
    user_record = db_user_record.fetchall()
    if not user_record:
        cur.execute(f"INSERT INTO user (id, first_name, username) VALUES (?, ?, ?)", (user.id, user.first_name, user.username))
        db_user_record = cur.execute(f"SELECT * FROM user WHERE id={user.id}")
        user_record = db_user_record.fetchall()

    con.commit()
    context.user_data['id'] = user_record[0][0]


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if not context.user_data.get('id'):
        get_user_id(update, context)
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def note_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /note is issued."""
    text = update.message.text[5:].strip(' ')
    topic, *text = text.split(":")
    topic = topic.upper()
    text = ':'.join(text)

    if not context.user_data.get('id'):
        get_user_id(update, context)

    user_id = context.user_data['id']

    try:
        cur.execute("INSERT INTO topic (user_id, name) VALUES (?, ?)", (user_id, topic))
    except:
        pass

    res = cur.execute("SELECT id FROM topic WHERE user_id=? AND name=?", (user_id, topic))
    topic_id = res.fetchall()[0][0]

    cur.execute("INSERT INTO note (topic_id, text) VALUES (?, ?)", (topic_id, text))
    con.commit()
    update.message.reply_text(f'Note "{text}" saved in topic {topic}!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ['TOKEN'])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("note", note_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
