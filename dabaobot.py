import time, settings, botmethods, dbhelper
from settings import settings
from botmethods import botmethods
from dbhelper import DBHelper

bot = botmethods()
set = settings()
db = DBHelper()

def handle_updates(updates, next_stage):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        if text == "/start":
            keyboard = set.build_keyboard()
            set.send_message("Hello! Are you very hungry?", chat, keyboard)
            return 'YESNO'
        elif text == 'Yes!' and next_stage == 'YESNO':
            set.send_message('Where would you like to order from?', chat)
            return 'WHERE'
        elif text == 'No!' and next_stage == 'YESNO':
            set.send_message('Here\'s a list of existing orders!', chat)
            set.send_message(bot.getAllOrders(chat), chat)
        elif text == 'What is this?':
            set.send_message('Hi! Welcome to FoodHitch, a goodwill based delivery system!', chat)
            set.send_message('You can choose to either place an order, or fulfill an order in return for a small tip.', chat)
            keyboard = set.build_keyboard()
            set.send_message("Hello! Are you hungry?", chat, keyboard)
            return 'YESNO'
        elif next_stage == 'WHERE':
            global location
            location = text
            set.send_message('What would you like to order?', chat)
            return 'WHAT'
        elif next_stage == 'WHAT':
            food = text
            set.send_message('Your order of {} from {} has been entered into the database!'.format(food, location), chat)
            db.add_order(chat, location, food)  ##
            set.send_message('Your current orders:', chat)
            set.send_message(bot.getOrderByChatID(chat), chat)
            keyboard = set.build_secondary_keyboard()
            set.send_message("Are you still hungry?", chat, keyboard)
            return 'YESNO'


def main():
    db.setup()
    last_update_id = None
    next_stage = 'INITIAL'
    location = 'INITIAL'
    while True:
        updates = set.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = set.get_last_update_id(updates) + 1
            next_stage = handle_updates(updates, next_stage)
        time.sleep(0.5)


if __name__ == '__main__':
    main()