import time, logging

from Controllers.settings import settings
from Controllers.botmethods import botmethods
from Controllers.dbhelper import DBHelper
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, Job)
from telegram.__main__ import main as tmain
from telegram import ReplyKeyboardMarkup
from datetime import time, timedelta

bots = botmethods()
set = settings()
db = DBHelper()

reply_keyboard = [['Feed myself!'], ['Help feed others!']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

reply_keyboard2 = [['Place an order'], ['View placed orders'], ['Main Menu']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)

reply_keyboard3 = [['Yes'], ['No'], ['Main Menu']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)

reply_keyboard4 = [['View All Orders'], ['View/Cancel Confirmed Orders'], ['Main Menu']]
markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True)

# reply_keyboard5 = [['Complete'], ['Cancel'], ['End']]
# markup5 = ReplyKeyboardMarkup(reply_keyboard5, one_time_keyboard=True)

MENU, SUBMENUHITCHEE, WHAT, WHERE, TIME, USERLOCATION, TIP, FINALIZE, \
CONFIRM, SUBMENUHITCHER, ACCEPT, DELIVERCONFIRM, CANCEL, CONFIRMCANCEL, \
CONFIRMREMOVE, CANCELHITCHEE, COMPLETEORCANCEL, COMPLETE, HITCHEECONFIRM  = range(19)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


### Starting Menu ###
def start(bot, update):
    if  update.message.chat.username is None:
        update.message.reply_text(
            "Hello and welcome to FoodHitch!\nIt seems like you do not have a Telegram Username.\n\nIn order to process your orders and ensure that communication between you and the deliverer is smooth, a username is needed.\n\nPlease create a Telegram Username before using me, thank you!\n(You can set your username in Settings.)")
    else:
        update.message.reply_text(
            "Welcome to FoodHitch, a goodwill based delivery system!\n\nYou can choose to either place an order, or fulfill an order in return for a small tip.(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
            reply_markup=markup)
        bots.removeExpiredOrders() #NOT elegant, might slow database down abit. TBD...
       # db.checkNumOfOrders(update.message.chat.id) ## To be done..
        return MENU

### Food Hitchee ###
def foodhitchee(bot, update):
    update.message.reply_text('Seems like you\'re hungry! \nPlease choose an option:', reply_markup=markup2)
    return SUBMENUHITCHEE


def what(bot, update):
    update.message.reply_text('What would you like to eat?\n(Between 4 to 30 characters. E.g. Mee Goreng, Chicken Rice..)')
    return WHERE


def where(bot, update, user_data):
    text = update.message.text
    if (len(text) > 3 and len(text) < 31):
        user_data['food'] = text
        update.message.reply_text('Where would you like to order it from?\n(Between 4 to 30 characters. E.g. North Spine Plaza, Canteen 14..)')
        return TIME
    else:
        update.message.reply_text("Your input is less than 4 characters. Please try again!")
        update.message.reply_text('What would you like to eat?\n(In more than 4 chars. E.g. Mee Goreng, Chicken Rice..)')
        return WHERE

def time(bot, update, user_data):
    text = update.message.text
    if (len(text) > 3 and len(text) < 31):
        user_data['location'] = text
        update.message.reply_text(
            'What date and time would you like the food to be sent at?(In DD MMM YYYY HHMM in 24hrs format)\n(E.g. 25 Oct 2017 1420)\nYou can make an order for 30 minutes after current time or up to 1 week in advance!\n')
        return USERLOCATION
    else:
        update.message.reply_text("Your input is less than 4 characters. Please try again!")
        update.message.reply_text('Where would you like to order it from?\n(Between 4 to 30 characters. E.g. North Spine Plaza, Canteen 14..)')
        return TIME

def userlocation(bot, update, user_data):
    text = update.message.text
    if (bots.checkDateFormat(text)):
        date = bots.convertStringToDate(text)
        future = date.now() + timedelta(minutes = 30)
        inbetween = date.now() + timedelta(weeks = 1)
        if (date >= future and date <= inbetween):
            user_data['time'] = date
            update.message.reply_text('Where would you like the food to be delivered to?\n(Between 4 to 30 characters. E.g. Hall 12, LT13..)')
            return TIP
        else:
            update.message.reply_text('Sorry! Your order has to be at least 30 minutes after current time up to a week''s advance booking.')
            update.message.reply_text(
                'What date and time would you like the food to be sent at?(In DD MMM YYYY HHMM in 24hrs format)\n(E.g. 25 Oct 2017 1420)\nYou can make an order for 30 minutes after current time or up to 1 week in advance!\n')
            return USERLOCATION
    else:
        update.message.reply_text('Sorry, invalid date or time! Please try again.')
        update.message.reply_text(
            'What date and time would you like the food to be sent at?(In DD MMM YYYY HHMM in 24hrs format)\n(E.g. 25 Oct 2017 1420)\nYou can make an order for 30 minutes after current time or up to 1 week in advance!\n')
        return USERLOCATION

def tip(bot, update, user_data):
    text = update.message.text
    if (len(text) > 3 and len(text) < 31):
        user_data['userlocation'] = text
        update.message.reply_text('How much would you like to tip your hitcher?\n(E.g. 2, 3.5) without the $ sign.')
        return FINALIZE
    else:
        update.message.reply_text("Your input is less than 4 characters. Please try again!")
        update.message.reply_text(
            'Where would you like to order it from?\n(Between 4 to 30 characters. E.g. North Spine Plaza, Canteen 14..)')
        return TIP

def finalize(bot, update, user_data):
    text = update.message.text
    if (bots.parseFloat(text)):
        if (float(text) > 0 and float(text) < 50):
            user_data['tip'] = text
            set.send_message('Food: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}hrs</b>\nDeliver to: <b>{}</b>\nTip: <b>${}</b>'.format(user_data["food"], user_data["location"], bots.convertToReadable(user_data["time"]), user_data["userlocation"], user_data["tip"]), update.message.chat.id)
            update.message.reply_text('Confirm order?', reply_markup=markup3)
            return CONFIRM
        else:
            update.message.reply_text('Please enter an amount between 1 and 50!')
            update.message.reply_text('How much would you like to tip your hitcher?\n(E.g. 2, 3.5) without the $ sign.')
            return FINALIZE
    else:
        update.message.reply_text('Please enter a valid number!')
        update.message.reply_text('How much would you like to tip your hitcher?\n(E.g. 2, 3.5) without the $ sign.')
        return FINALIZE


def addorder(bot, update, user_data):
    userid = update.message.chat.id
    username = update.message.chat.username
    db.add_order(userid, user_data["location"], user_data["food"], user_data["userlocation"], user_data["time"],
                 username, user_data["tip"])
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
    placedorders = bots.getUnconfirmedOrdersByChatID(update.message.chat.id)
    if placedorders is not None:
        update.message.reply_text('Here''s a list of your placed orders!')
        set.send_message(placedorders, update.message.chat.id)
        return CONFIRMREMOVE
    else:
        update.message.reply_text('You have no open orders! Please place an order first.')
        update.message.reply_text('Seems like you\'re hungry! \nPlease choose an option:', reply_markup=markup2)
        return SUBMENUHITCHEE

def confirmRemovePlacedOrder(bot, update, user_data):
    user_data['placed'] = update.message.text
    if bots.checkPlacedOrdersByChatID(user_data['placed'], update.message.chat.id) == 'SUCCESSFUL':
        db.removePlacedOrder(user_data['placed'])
        update.message.reply_text('Order removed from list.')
        user_data.clear()
        update.message.reply_text(
        "Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
        reply_markup=markup)
        return MENU
    else:
        update.message.reply_text('Invalid Order ID! Please try again.')
        update.message.reply_text('Here''s a list of your placed orders!')
        set.send_message(bots.getUnconfirmedOrdersByChatID(update.message.chat.id), update.message.chat.id)
        return CONFIRMREMOVE

def pendingOrders(bot, update):
        placedorders = bots.getPendingOrdersByChatID(update.message.chat.id)
        if placedorders is not None:
            update.message.reply_text('Here''s a list of your pending orders!')
            set.send_message(placedorders, update.message.chat.id)
            return CANCELHITCHEE

        else:
            update.message.reply_text('You have no pending orders! Please place an order first.')
            update.message.reply_text('Seems like you\'re hungry! \nPlease choose an option:', reply_markup=markup2)
            return SUBMENUHITCHEE

def confirmCancelPendingOrder(bot, update, user_data):
            user_data['placed'] = update.message.text
            if bots.checkPendingOrdersByChatID(user_data['placed'], update.message.chat.id) == 'SUCCESSFUL':
                db.setStatus(3, user_data['placed'])
                update.message.reply_text('Order cancelled successfully!')
                set.send_message('The order of: \n' + bots.getOrderByOrderID(user_data['placed']) + '\n has been cancelled by hitchee.', bots.getSenderChatIdByOrderId(user_data['placed']))
                user_data.clear()
                update.message.reply_text(
                    "Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
                    reply_markup=markup)
                return MENU
            else:
                update.message.reply_text('Invalid Order ID! Please try again.')
                update.message.reply_text('Here''s a list of your placed orders!')
                set.send_message(bots.getUnconfirmedOrdersByChatID(update.message.chat.id), update.message.chat.id)
                return CONFIRMREMOVE

### Food Hitcher ###
def foodhitcher(bot, update):
    update.message.reply_text('Thank you for making hungry people happy! \nPlease choose an option:',
                              reply_markup=markup4)
    return SUBMENUHITCHER

def vieworders(bot, update):
    allOrders = bots.getAllOrders()
    if allOrders == "There are currently no orders!":
        update.message.reply_text('There are currently no orders!')
        update.message.reply_text('Thank you for making hungry people happy! \nPlease choose an option:',
                                  reply_markup=markup4)
        return SUBMENUHITCHER
    else:
        update.message.reply_text('Here''s a list of existing orders!')
        set.send_message(allOrders, update.message.chat.id)
        return ACCEPT

def acceptorder(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    if bots.checkOrders(user_data['choice']) == 'SUCCESSFUL':
        if update.message.chat.id == bots.getChatIdByOrderId(user_data['choice']):
            bots.checkOrders(user_data['choice'])
            update.message.reply_text('Please confirm following order to be accepted:', reply_markup=markup3)
            set.send_message(bots.getOrderByOrderID(user_data['choice']), update.message.chat.id)
            return DELIVERCONFIRM
        else:
            update.message.reply_text('You cannot accept your own order! Please try again.')
            update.message.reply_text('Here''s a list of existing orders!')
            set.send_message(bots.getAllOrders(), update.message.chat.id)
            return ACCEPT
    else:
        update.message.reply_text('Invalid Order ID! Please try again.')
        update.message.reply_text('Here''s a list of existing orders!')
        set.send_message(bots.getAllOrders(), update.message.chat.id)
        return ACCEPT

def repeatdelivery(bot, update, user_data):
    user_data.clear()
    update.message.reply_text('Here''s a list of existing orders!')
    set.send_message(bots.getAllOrders(update.message.chat.id), update.message.chat.id)
    return ACCEPT

def confirmorder(bot, update, user_data):
    db.bindSenderToOrder(update.message.chat.username, update.message.chat.id, user_data['choice'])
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
    pendingorders = bots.getPendingOrdersByUsername(update.message.chat.username)
    if pendingorders is not None:
        update.message.reply_text('Here are your pending orders!')
        set.send_message(bots.getPendingOrdersByUsername(update.message.chat.username), update.message.chat.id)
        update.message.reply_text('Please enter order ID you would like to cancel or tap on /home to return to home page.')
        return CANCEL
    else:
        update.message.reply_text('You have not accepted any orders yet!')
        update.message.reply_text('Thank you for making hungry people happy! \nPlease choose an option:',
                                  reply_markup=markup4)
        return SUBMENUHITCHER

# def completerequestorderid(bot, update):
#     update.message.reply_text('Please enter order ID you would like to complete:')
#     return COMPLETE
#
# def cancelrequestorderid(bot, update):
#     update.message.reply_text('Please enter order ID you would like to cancel:')
#     return CANCEL

# def completeorder(bot, update, user_data):
#     text = update.message.text
#     user_data['order'] = text
#     if bots.checkOrderToCancel(user_data['order'], update.message.chat.username) == 'SUCCESSFUL':
#         update.message.reply_text('Awaiting confirmation from the other party..')
#         set.send_message(
#             '@' + bots.getSenderByOrderId(user_data['order']) + ' would like to confirm the following order:',
#             bots.getChatIdByOrderId(user_data['order']))
#         set.send_message(bots.getOrderByOrderID(user_data['order']), bots.getChatIdByOrderId(user_data['order']))
#         set.send_message('Please confirm.', bots.getChatIdByOrderId(user_data['order']), reply_markup=markup3)
#         return HITCHEECONFIRM


def cancelorders(bot, update, user_data):
    text = update.message.text
    user_data['order'] = text
    if bots.checkOrderToCancel(user_data['order'], update.message.chat.username) == 'SUCCESSFUL':
        update.message.reply_text('Please confirm following order to be cancelled:', reply_markup=markup3)
        set.send_message(bots.getOrderByOrderID(user_data['order']), update.message.chat.id)
        return CONFIRMCANCEL
    else:
        update.message.reply_text('Invalid Order ID! Please try again.')
        update.message.reply_text('Here are your pending orders!')
        set.send_message(bots.getPendingOrdersByChatID(update.message.chat.id), update.message.chat.id)
        update.message.reply_text('Please enter order ID that you would like to cancel or tap on /home to return to home page.')
        return CANCEL

def confirmcancel(bot, update, user_data):
    chatid = bots.getChatIdByOrderId(user_data['order'])
    db.setStatus(0, user_data['order'])
    update.message.reply_text('Order cancelled successfully!')
    set.send_message('Your order of: \n' + bots.getOrderByOrderID(user_data['order']) + '\nhas been cancelled. It has been placed back on the list until expiry. Please try again!', chatid)
    user_data.clear()
    update.message.reply_text(
        "Hello and welcome to FoodHitch!\n(At any point of time, type /cancel to terminate my service)\n\nNow.. What would you like to do?",
        reply_markup=markup)
    return MENU

def returncancel(bot, update):
    #set.send_message(bots.getPendingOrdersByChatID(update.message.chat.id), update.message.chat.id)
    update.message.reply_text('Please enter order ID you would like to cancel or tap on /home to return to home page.')
    return CANCEL

# def hitcheeconfirm(bot, update, user_data):


## Misc ###
def cancel(bot, update, user_data):
    update.message.reply_text('Thank you for using me. /start me up soon again yeah?')
    user_data.clear()
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
    #updater = Updater("387099409:AAFmM5sismztGNYvfUo388Bn9QeEhUUcce8")  # Dev environment
    updater = Updater("422679288:AAFmt0jTQIUs-9aZkTMCJ2AhDHWDaToYk3Y") # Updater takes in bot token, runs in separate thread and handles updates from different telegram users.
    dp = updater.dispatcher
    conv_handler = ConversationHandler( #Handles different commands, states. For e.g. "Food Hitchee" Is under MENU state
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [RegexHandler('^(Feed myself!)$',
                                foodhitchee),
                   RegexHandler('^(Help feed others!)$',
                                foodhitcher),
                   RegexHandler('^(Help)$',
                                help)
                   ],
            #### Food Hitchee ####
            SUBMENUHITCHEE: [RegexHandler('^Place an order$',
                                          what),
                             RegexHandler('^View placed orders$',
                                          placedorders),
                             RegexHandler('^View pending orders$',
                                          pendingOrders)
                             ],
            WHERE: [MessageHandler(Filters.text,
                                   where, pass_user_data=True)],

            TIME: [MessageHandler(Filters.text,
                                  time, pass_user_data=True)],

            USERLOCATION: [MessageHandler(Filters.text,
                                          userlocation, pass_user_data=True)],

            TIP: [MessageHandler(Filters.text,
                                          tip, pass_user_data=True)],

            FINALIZE: [MessageHandler(Filters.text,
                                      finalize, pass_user_data=True)],

            CONFIRM: [RegexHandler('^Yes$', addorder, pass_user_data=True),
                      RegexHandler('^No$', repeatorder, pass_user_data=True)],

            CONFIRMREMOVE: [MessageHandler(Filters.text,
                                      confirmRemovePlacedOrder, pass_user_data=True)],

            CANCELHITCHEE: [MessageHandler(Filters.text,
                                           confirmCancelPendingOrder, pass_user_data=True)],

            #### Food Hitcher ####
            SUBMENUHITCHER: [RegexHandler('^View All Orders$',
                                          vieworders),
                             RegexHandler('^View/Cancel Confirmed Orders$',
                                          confirmedorders)
                             ],
            ACCEPT: [MessageHandler(Filters.text,
                                    acceptorder, pass_user_data=True)],


            # COMPLETEORCANCEL: [RegexHandler('^Complete$', completerequestorderid),
            #                  RegexHandler('^Cancel$', cancelrequestorderid)],
            #
            # COMPLETE: [MessageHandler(Filters.text,
            #                          completeorder, pass_user_data=True)],

            CANCEL: [MessageHandler(Filters.text,
                                    cancelorders, pass_user_data=True)],

            CONFIRMCANCEL: [RegexHandler('^Yes$', confirmcancel, pass_user_data=True),
                             RegexHandler('^No$', returncancel)],

            # HITCHEECONFIRM: [MessageHandler(Filters.text,
            #                          hitcheeconfirm, pass_user_data=True)],

            DELIVERCONFIRM: [RegexHandler('^Yes$', confirmorder, pass_user_data=True),
                             RegexHandler('^No$', repeatdelivery, pass_user_data=True)]

        },

        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True), #These commands are to terminate, return or more specifically do something if the other states return "FALSE".
                   RegexHandler('^Main Menu$', start),
                   CommandHandler('home', start)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    tmain()
    main()
