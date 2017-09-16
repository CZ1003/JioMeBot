import time

from Controllers.settings import settings
from Controllers.botmethods import botmethods
from Controllers.dbhelper import DBHelper

bot = botmethods()
set = settings()
db = DBHelper()

def handle_updates(updates, next_stage):
    global location, usertime, userlocation, orderid, user, food
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        if 'username' not in update['message']["chat"]:
            user = ""
        else:
            user = update["message"]["chat"]["username"]
        if text == "/start" and user == "":
            set.send_message('Hello and welcome to FoodHitch!\nIt seems like you do not have a Telegram Username.\nIn order to process your orders and ensure that communication between you and the deliverer is smooth, a username is needed.\nPlease create a Telegram Username before using me, thank you!',chat)
            return 'Initial'
        elif text == "/start":
            keyboard = set.build_keyboard(1)
            set.send_message('Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?', chat, keyboard)
            return 'YESNO'
        elif text == 'Place an order' and next_stage == 'YESNO':
            set.send_message('What would you like to eat?', chat)
            return 'WHERE'
        elif text == 'What is this?':
            set.send_message('Hi! Welcome to FoodHitch, a goodwill based delivery system!\n' \
           'You can choose to either place an order, or fulfill an order in return for a small tip.', chat)
            keyboard = set.build_keyboard(1)
            set.send_message('Hello and welcome to FoodHitch!\nWhat would you like to do?', chat, keyboard)
            return 'YESNO'
        elif next_stage == 'WHERE':
            location = text
            set.send_message('Where would you like to order it from?', chat)
            return 'TIME'
        elif next_stage == 'TIME':
            usertime = text
            set.send_message('What time would you like the food to be sent at?', chat)
            return 'USERLOCATION'
        elif next_stage == 'USERLOCATION':
            userlocation = text
            set.send_message('Where would you like the food to be delivered to?', chat)
            return 'FINALIZE'
        elif next_stage == 'FINALIZE':
            food = text
            set.send_message('Your order of {} from {} has been entered into the database!\nGood luck in getting a Food Hitch!'.format(location, food), chat)
            db.add_order(chat, location, food, userlocation, usertime, user)
            set.send_message('Your current orders:', chat)
            set.send_message(bot.getOrderByChatID(chat), chat)
            keyboard = set.build_keyboard(2)
            set.send_message('Are you still hungry?', chat, keyboard)
            return 'YESNO'
        elif text == 'No!' and next_stage == 'YESNO':
            keyboard = set.build_keyboard(1)
            set.send_message('Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?',chat, keyboard)
            return 'YESNO'
        elif text == '/cancel':
            set.send_message('Thank you for using me. /start me up soon again yeah?', chat)
            return 'INITIAL'
        # Deliver orders
        elif text == 'Deliver orders' and next_stage == 'YESNO':
            set.send_message('Here\'s a list of existing orders!', chat)
            set.send_message(bot.getAllOrders(chat), chat)
            return 'ACCEPT'
        elif next_stage == 'ACCEPT':
            orderid = text
            set.send_message('Please confirm following order to be accepted:', chat)
            keyboard = set.build_keyboard(2)
            set.send_message(bot.getOrderByOrderID(orderid), chat, keyboard)
            return 'DELIVERCONFIRM'
        elif text == 'No!' and next_stage == 'DELIVERCONFIRM':
            keyboard = set.build_keyboard(1)
            set.send_message('Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?',
                chat, keyboard)
            return 'YESNO'
        elif text == 'Yes!' and next_stage == 'DELIVERCONFIRM':
            db.bindSenderToOrder(user, orderid)
            set.send_message('Congratulations! You have accepted this order. Please contact @' + bot.getUsernameByOrderId(orderid) + ' for further communication.', chat)
            db.setStatus(1, orderid)
            set.send_message('Congratulations! Your order has been accepted!\nThis order has been placed on hold and will not appear in main list.\nPlease contact @' + user + ' for further communication.', bot.getChatIdByOrderId(orderid))

def main():
    db.setup()
    last_update_id = None
    next_stage = 'INITIAL'
    while True:
        updates = set.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = set.get_last_update_id(updates) + 1
            next_stage = handle_updates(updates, next_stage)
        time.sleep(0.5)


if __name__ == '__main__':
    main()