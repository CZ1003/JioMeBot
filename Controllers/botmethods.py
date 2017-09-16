from Controllers.dbhelper import DBHelper

db = DBHelper()

class botmethods:
    def __init__(self):
        pass

    def getAllOrders(self, chat): #Function to get all orders
        list = []
        for (a, b, c, d, e) in db.get_all_orders():  ##
            list.append('ID: <b>{}</b> Food: <b>{}</b> from <b>{}</b> - Time: <b>{}</b> Deliver to: <b>{}</b>'.format(a, b, c, d, e))
            message = "\n".join(list) + '\n\nPlease key in a valid order ID!'
        if not list:
            message = "There are currently no orders!"
        return message

    def getOrderByChatID(self, chat):  # Function to get order by ID
        list = []
        for (a, b, c, d, e) in db.get_order(chat):  ##
                list.append('ID: <b>{}</b> Food: <b>{}</b> from <b>{}</b> - Time: <b>{}</b> Deliver to: <b>{}</b>'.format(a, b, c, d, e))
                message = "\n".join(list)
        return message

    def getOrderByOrderID(self, orderId):  # Function to get order by ID
        list = []
        for (a, b, c, d, e) in db.getOrderByOrderID(orderId):  ##
            list.append('ID: <b>{}</b> Food: <b>{}</b> from <b>{}</b> - Time: <b>{}</b> Deliver to: <b>{}</b>'.format(a, b, c, d, e))
            message = "\n".join(list)
        return message

    def getChatIdByOrderId(self, orderId):  # Function to get order by ID
        list = []
        for (a, b) in db.getChatIdByOrderId(orderId):  ##
            list.append('{}'.format(a, b))
            message = "\n".join(list)
        return message

    def getUsernameByOrderId(self, orderId):  # Function to get order by ID
        list = []
        for (a,b) in db.getUsernameByOrderId(orderId):  ##
            list.append('{}'.format(a, b))
            message = "\n".join(list)
        return message