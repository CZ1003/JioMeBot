import time, logging

from Controllers.settings import settings
from Controllers.botmethods import botmethods
from Controllers.dbhelper import DBHelper
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, Job)
from telegram.__main__ import main as tmain
from telegram import ReplyKeyboardMarkup

bots = botmethods()
set = settings()
db = DBHelper()

reply_keyboard = [['Food Hitchee'], ['Food Hitcher'],
                  ['Help'], ['End']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

reply_keyboard2 = [['Place an order'], ['View placed orders'], ['End']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)

reply_keyboard3 = [['Yes'], ['No'], ['End']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)

reply_keyboard4 = [['View All Orders'], ['View Confirmed Orders'], ['End']]
markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True)

MENU, SUBMENUHITCHEE, WHAT, WHERE, TIME, USERLOCATION, FINALIZE, CONFIRM, SUBMENUHITCHER, ACCEPT, DELIVERCONFIRM = range(
    11)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


### Starting Menu ###
def start(bot, update):
    if  update.message.chat.username is None:
        update.message.reply_text(
            "Hello and welcome to FoodHitch!\nIt seems like you do not have a Telegram Username.\nIn order to process your orders and ensure that communication between you and the deliverer is smooth, a username is needed.\nPlease create a Telegram Username before using me, thank you!\n(You can set your username in Settings.)")
    else:
        update.message.reply_text(
            "Hello and welcome to FoodHitch, bitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
            reply_markup=markup)
        return MENU


### Food Hitchee ###
def foodhitchee(bot, update):
    update.message.reply_text('Seems like you\'re hungry! \nPlease choose an option:', reply_markup=markup2)
    return SUBMENUHITCHEE


def what(bot, update):
    update.message.reply_text('What would you like to eat?\n(E.g. Mee Goreng, Chicken Rice..)')
    return WHERE


def where(bot, update, user_data):
    text = update.message.text
    user_data['food'] = text
    update.message.reply_text('Where would you like to order it from?\n(E.g. North Spine Plaza, Canteen 14..)')
    return TIME


def time(bot, update, user_data):
    text = update.message.text
    user_data['location'] = text
    update.message.reply_text('What time would you like the food to be sent at?\n(E.g. 2AM, 4PM..)')
    return USERLOCATION


def userlocation(bot, update, user_data):
    text = update.message.text
    user_data['time'] = text
    update.message.reply_text('Where would you like the food to be delivered to?\n(E.g. Hall 12, LT13..)')
    return FINALIZE


def finalize(bot, update, user_data):
    text = update.message.text
    user_data['userlocation'] = text
    set.send_message('Food: <b>{}</b> from <b>{}</b> at <b>{}</b> to <b>{}</b>.'.format(user_data["food"], user_data["location"], user_data["time"], user_data["userlocation"]), update.message.chat.id)
    update.message.reply_text('Confirm order?', reply_markup=markup3)
    return CONFIRM


def addorder(bot, update, user_data):
    userid = update.message.chat.id
    username = update.message.chat.username
    db.add_order(userid, user_data["location"], user_data["food"], user_data["userlocation"], user_data["time"],
                 username)
    update.message.reply_text(
        'Your order of {} from {} has been entered into the database!\nGood luck in getting a Food Hitch!'.format(
            user_data["food"], user_data["location"]))
    user_data.clear()
    update.message.reply_text(
        "Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
        reply_markup=markup)
    return MENU

def repeatorder(bot, update, user_data):
    user_data.clear()
    update.message.reply_text('Seems like you\'re hungry! \nPlease choose an option:', reply_markup=markup2)
    return SUBMENUHITCHEE

def placedorders(bot, update):
    update.message.reply_text('Under construction!')
    update.message.reply_text(
        "Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
        reply_markup=markup)
    return MENU


### Food Hitcher ###
def foodhitcher(bot, update):
    update.message.reply_text('Thank you for making hungry people happy! \nPlease choose an option:',
                              reply_markup=markup4)
    return SUBMENUHITCHER


def vieworders(bot, update):
    update.message.reply_text('Here''s a list of existing orders!')
    set.send_message(bots.getAllOrders(update.message.chat.id), update.message.chat.id)
    return ACCEPT


def acceptorder(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    if bots.checkOrders(user_data['choice']) == 'SUCCESSFUL':
        bots.checkOrders(user_data['choice'])
        update.message.reply_text('Please confirm following order to be accepted:', reply_markup=markup3)
        set.send_message(bots.getOrderByOrderID(user_data['choice']), update.message.chat.id)
        return DELIVERCONFIRM
    else:
        update.message.reply_text('Invalid Order ID! Please try again.')
        update.message.reply_text('Here''s a list of existing orders!')
        set.send_message(bots.getAllOrders(update.message.chat.id), update.message.chat.id)
        return ACCEPT

def repeatdelivery(bot, update, user_data):
    user_data.clear()
    update.message.reply_text('Here''s a list of existing orders!')
    set.send_message(bots.getAllOrders(update.message.chat.id), update.message.chat.id)
    return ACCEPT

def confirmorder(bot, update, user_data):
    db.bindSenderToOrder(update.message.chat.id, user_data['choice'])
    set.send_message('Congratulations! You have accepted this order.\nOrder Details:\n\n' + bots.getOrderByOrderID(
        user_data['choice']) + '\n\nPlease contact @' + bots.getUsernameByOrderId(
        user_data['choice']) + ' for further communication.', update.message.chat.id)
    db.setStatus(1, user_data['choice'])
    set.send_message('Congratulations! Your order has been accepted!\nOrder Details:\n\n' + bots.getOrderByOrderID(
        user_data[
            'choice']) + '\n\nThis order has been placed on hold and will not appear in main list.\nPlease contact @' + update.message.chat.username + ' for further communication.',
                     bots.getChatIdByOrderId(user_data['choice']))

    user_data.clear()
    update.message.reply_text(
        "Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
        reply_markup=markup)
    return MENU


def confirmedorders(bot, update):
    update.message.reply_text('Under construction!')
    update.message.reply_text(
        "Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
        reply_markup=markup)
    return MENU


## Misc ###
def cancel(bot, update, user_data):
    user_data.clear()
    update.message.reply_text('Thank you for using me. /start me up soon again yeah?')
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def help(bot, update):
    update.message.reply_text('Hi! Welcome to FoodHitch, a goodwill based delivery system!\n' \
                              'You can choose to either place an order, or fulfill an order in return for a small tip.')
    update.message.reply_text(
        'Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?',
        reply_markup=markup)
    return MENU

### Main ###
def main():
    db.setup()
    updater = Updater("387099409:AAFmM5sismztGNYvfUo388Bn9QeEhUUcce8")
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [RegexHandler('^(Food Hitchee)$',
                                foodhitchee),
                   RegexHandler('^(Food Hitcher)$',
                                foodhitcher),
                   RegexHandler('^(Help)$',
                                help)
                   ],
            #### Food Hitchee ####
            SUBMENUHITCHEE: [RegexHandler('^Place an order$',
                                          what),
                             RegexHandler('^View placed orders$',
                                          placedorders)
                             ],
            WHERE: [MessageHandler(Filters.text,
                                   where, pass_user_data=True)],

            TIME: [MessageHandler(Filters.text,
                                  time, pass_user_data=True)],

            USERLOCATION: [MessageHandler(Filters.text,
                                          userlocation, pass_user_data=True)],

            FINALIZE: [MessageHandler(Filters.text,
                                      finalize, pass_user_data=True)],

            CONFIRM: [RegexHandler('^Yes$', addorder, pass_user_data=True),
                      RegexHandler('^No$', repeatorder, pass_user_data=True)],

            #### Food Hitcher ####
            SUBMENUHITCHER: [RegexHandler('^View All Orders$',
                                          vieworders),
                             RegexHandler('^View Confirmed Orders$',
                                          confirmedorders)
                             ],
            ACCEPT: [MessageHandler(Filters.text,
                                    acceptorder, pass_user_data=True)],

            DELIVERCONFIRM: [RegexHandler('^Yes$', confirmorder, pass_user_data=True),
                             RegexHandler('^No$', repeatdelivery, pass_user_data=True)]

        },

        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True),
                   RegexHandler('^End$', cancel, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    tmain()
    main()
