import time
import urllib
import json
import requests
from dbhelper import DBHelper


db = DBHelper()
TOKEN = "422679288:AAFmt0jTQIUs-9aZkTMCJ2AhDHWDaToYk3Y"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def build_keyboard():
    keyboard = [[item] for item in ['Yes!', 'No!', 'What is this?']]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def build_secondary_keyboard():
    keyboard = [[item] for item in ['Yes!', 'No!']]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def handle_updates(updates, next_stage):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        if text == "/start":
            keyboard = build_keyboard()
            send_message("Hello! Are you hungry?", chat, keyboard)
            return 'YESNO'
        elif text == 'Yes!' and next_stage == 'YESNO':
            send_message('Where would you like to order from?', chat)
            return 'WHERE'
        elif text == 'No!' and next_stage == 'YESNO':
            send_message('Here\'s a list of existing orders!', chat)
            list = []
            for (x, y) in db.get_all_orders():  ##
                list.append('{} from {}'.format(x, y))
            message = "\n".join(list)
            send_message(message, chat)
        elif text == 'What is this?':
            send_message('Hi! Welcome to FoodHitch, a goodwill based delivery system!', chat)
            send_message('You can choose to either place an order, or fulfill an order in return for a small tip.', chat)
            keyboard = build_keyboard()
            send_message("Hello! Are you hungry?", chat, keyboard)
            return 'YESNO'
        elif next_stage == 'WHERE':
            global location
            location = text
            send_message('What would you like to order?', chat)
            return 'WHAT'
        elif next_stage == 'WHAT':
            food = text
            send_message('Your order of {} from {} has been entered into the database!'.format(food, location), chat)
            db.add_order(chat, location, food)  ##
            list = []
            for (x, y) in db.get_order(chat):  ##
                list.append('{} from {}'.format(x, y))
            message = "\n".join(list)
            send_message('Your current orders:', chat)
            send_message(message, chat)
            keyboard = build_secondary_keyboard()
            send_message("Are you still hungry?", chat, keyboard)
            return 'YESNO'


def main():
    db.setup()
    last_update_id = None
    next_stage = 'INITIAL'
    location = 'INITIAL'
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            next_stage = handle_updates(updates, next_stage)
        time.sleep(0.5)


if __name__ == '__main__':
    main()