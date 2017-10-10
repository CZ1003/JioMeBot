from Controllers.dbhelper import DBHelper
from dateutil.parser import parse
from datetime import datetime, timedelta
from Controllers.settings import settings
import pytz

db = DBHelper()
set = settings()
class botmethods:
    def __init__(self):
        pass

    def getAllPlacedOrders(self, chatid): #Function to get all orders
        message = None
        list = []
        for (a, b, c, d, e, f) in db.get_all_placedorderswithoutownorder(chatid):  ##
            list.append('ID: <b>{}</b>\nFood: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}hrs</b>\nDeliver to: <b>{}</b>\nTip: <b>${}</b>\n----------------------------------------'.format(a, b, c, self.convertStringToDateFromDB(d), e, f))
            message = "\n".join(list) + '\n\nPlease key in a valid order ID to accept or tap on /home to return to home page.'
        if not list:
            message = "There are currently no orders!"
        return message

    def getOrderByChatID(self, chat):  # Function to get order by ID
        message = None
        list = []
        for (a, b, c, d, e, f) in db.get_order(chat):  ##
            list.append('ID: <b>{}</b>\nFood: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}hrs</b>\nDeliver to: <b>{}</b>\nTip: <b>${}</b>\n----------------------------------------'.format(a, b, c, self.convertStringToDateFromDB(d), e, f))
            message = "\n".join(list)
        return message

    def getPendingOrdersByChatID(self, chat):  # Function to get order by ID
        message = None
        list = []
        for (a, b, c, d, e, f) in db.get_order(chat):  ##
            list.append(
                'ID: <b>{}</b>\nFood: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}hrs</b>\nDeliver to: <b>{}</b>\nTip: <b>${}</b>\n----------------------------------------'.format(
                    a, b, c, self.convertStringToDateFromDB(d), e, f))
            message = "\n".join(list)
        return message

    def getOrderByOrderID(self, orderId):  # Function to get order by ID
        message = None
        list = []
        for (a, b, c, d, e, f) in db.getOrderByOrderID(orderId):  ##
            list.append(
                'ID: <b>{}</b>\nFood: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}hrs</b>\nDeliver to: <b>{}</b>\nTip: <b>${}</b>\n----------------------------------------'.format(
                    a, b, c, self.convertStringToDateFromDB(d), e, f))
            message = "\n".join(list)
        return message

    def getChatIdByOrderId(self, orderId):  # Function to get order by ID
        message = None
        list = []
        for (a, b) in db.getChatIdByOrderId(orderId):  ##
            list.append('{}'.format(a, b))
            message = "\n".join(list)
        return message

    def getUsernameByOrderId(self, orderId):  # Function to get order by ID
        message = None
        list = []
        for (a,b) in db.getUsernameByOrderId(orderId):  ##
            list.append('{}'.format(a, b))
            message = "\n".join(list)
        return message

    def getSenderByOrderId(self, orderId):  # Function to get order by ID
        message = None
        list = []
        for (a,b) in db.getsenderByOrderId(orderId):  ##
            list.append('{}'.format(a, b))
            message = "\n".join(list)
        return message

    def getPendingOrdersByUsername(self, username):
        message = None
        list = []
        for (a, b,c, d, e, f, g) in db.getPendingOrdersByUsername(username):  ##
            list.append(
                'ID: <b>{}</b>\nFood: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}hrs</b>\nDeliver to: <b>{}</b>\nTip: <b>${}</b>\nReceiver''s username: @{}\n----------------------------------------'.format(
                    a, b, c, self.convertStringToDateFromDB(d), e, f, g))
            message = "\n".join(list)
        return message

    def getSenderChatIdByOrderId(self, order_id):
        message = None
        list = []
        for (a, b) in db.getSenderChatIDbyOrderId(order_id):  ##
            list.append('{}'.format(a, b))
            message = "\n".join(list)
        return message

    def getUnconfirmedOrdersByChatID(self, chat_id):
        message = None
        list = []
        for (a, b,c, d, e, f) in db.get_unconfirmed_orders_by_chat_id(chat_id):  ##
            list.append(
                'ID: <b>{}</b>\nFood: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}hrs</b>\nDeliver to: <b>{}</b>\nTip: <b>${}</b>\n----------------------------------------'.format(
                    a, b, c, self.convertStringToDateFromDB(d), e, f))
            message = "\n".join(list) + '\n\nPlease key in a valid order ID to delete or tap on /home to return to home page.'
        return message

    def getPendingOrdersByChatID(self, chatId):  # Function to get order by ID
        message = None
        list = []
        for (a, b, c, d, e,f, g) in db.get_all_pendingorders_by_chat_id(chatId):  ##
            list.append(
                'ID: <b>{}</b>\nFood: <b>{}</b>\nLocation: <b>{}</b>\nDate and Time: <b>{}</b>hrs\nDeliver to: <b>{}</b>\nTip: <b>${}</b>\nSender username: @{}\n----------------------------------------'.format(
                    a, b, c, self.convertStringToDateFromDB(d), e, f, g))
            message = "\n".join(list)
        return message

### Checking ###
    def parseFloat(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def checkOrderToCancel(self, orderId, username):
        success = "UNSUCCESSFUL"
        for (a, b, c, d, e, f) in db.getPendingOrderByOrderID(orderId, username):  ##
            try:
                orderidparse = int(orderId)
                if a == orderidparse:
                    success = "SUCCESSFUL"
                    return success
                else:
                    success = "UNSUCCESSFUL"
            except ValueError:
                return success
        return success

    def checkOrders(self, orderId):  # Function to get all orders
        success = "UNSUCCESSFUL"
        for (a, b, c, d, e, f) in db.get_all_orders():  ##
            try:
                orderidparse = int(orderId)
                if a == orderidparse:
                    success = "SUCCESSFUL"
                    return success
                else:
                   success = "UNSUCCESSFUL"
            except ValueError:
                return success
        return success

    def checkPlacedOrdersByChatID(self, orderId, chatId):  # Function to get all orders
        success = "UNSUCCESSFUL"
        for (a, b, c, d, e, f) in db.getAllPlacedOrdersByChatID(chatId, orderId ):  ##
            try:
                orderidparse = int(orderId)
                if a == orderidparse:
                    success = "SUCCESSFUL"
                    return success
                else:
                   success = "UNSUCCESSFUL"
            except ValueError:
                return success
        return success

    def checkPendingOrdersByChatID(self, orderId, chatId):  # Function to get all orders
        success = "UNSUCCESSFUL"
        for (a, b, c, d, e,f, g) in db.get_all_pendingorders_by_chat_id(chatId):  ##
            try:
                orderidparse = int(orderId)
                if a == orderidparse:
                    success = "SUCCESSFUL"
                    return success
                else:
                   success = "UNSUCCESSFUL"
            except ValueError:
                return success
        return success

    def checkInt(self, i):
        try:
            int(i)
            return True
        except ValueError:
            return False

    def checkDate(self, i):
        try:
           parse(i)
           return True
        except ValueError:
           return False

    def checkDateFormat(self, i):
        try:
            datetime.strptime(i, '%d %b %Y %H%M')
            return True
        except ValueError:
            return False

    def convertToReadable(self, i):
        try:
            return datetime.strftime(i, '%d %b %Y %H%M')
        except ValueError:
            return False

    def convertStringToDateFromDB(self, i):
        try:
            date = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
            return datetime.strftime(date, '%d %b %Y %H%M')
        except ValueError:
            return False

    def convertStringToDate(self, i):
        try:
            return datetime.strptime(i, '%d %b %Y %H%M')
        except ValueError:
            return False

    def removeExpiredOrders(self):
            for (a, b, c, d, e, f, g) in db.get_all_orders():  ##
                date = datetime.strptime(e, '%Y-%m-%d %H:%M:%S')
                singapore = pytz.timezone('Asia/Kuala_Lumpur')
                singaporedbdate = date.astimezone(singapore) - timedelta(hours = 8)
                singaporetimezone = datetime.now().astimezone(singapore)
                if (singaporetimezone >= singaporedbdate):
                     set.send_message("Your order of: ", a)
                     set.send_message(self.getOrderByOrderID(b), a)
                     set.send_message("has expired! Please place a new order.")
                     db.removeExpiredOrders(e)


