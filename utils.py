from datetime import datetime
import os
import requests
import sys

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(__file__))
class Utils: 
    def log(msg):
        # f = open(os.path.join(Instance.LOG_DIR_PATH, "file.log"), "a")
        f = open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__))), "log.log"), "a")
        f.write(f"{datetime.today()} --- {msg}\n")
        f.close()

    def send_message_to_telegram(chat_id, text, reply_markup=None):
        TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage"

        if reply_markup:
            payload = {'chat_id': chat_id, 'text': text, "reply_markup": reply_markup}
        else:
            payload = {'chat_id': chat_id, 'text': text}
        r = requests.post(TELEGRAM_SEND_MESSAGE_URL, json=payload)

        print(r.json())