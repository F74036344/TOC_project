import sys

import telegram
from flask import Flask, request

API_TOKEN = '360313119:AAGJOkRmXF2wxcqwEkujI47qrRotks7XS2I'
# You can get the API token from the BotFather on the Telegram
WEBHOOK_URL = 'https://Your URL/hook'
# e.g. 'https://Your URL/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        text = update.message.text

        update.message.reply_text(text)
    return 'ok'


if __name__ == "__main__":
    _set_webhook()
    app.run()
