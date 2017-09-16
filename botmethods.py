from dbhelper import DBHelper

db = DBHelper()

class botmethods:
    def __init__(self):
        pass

    def getAllOrders(self, chat): #Function to get all orders
        list = []
        for (x, y, z) in db.get_all_orders():  ##
            list.append('Order ID: {} - {} from {}'.format(x, y, z))
        message = "\n".join(list)
        return message

    def getOrderByChatID(self, chat):  # Function to get order by ID
        list = []
        for (x, y, z) in db.get_order(chat):  ##
            list.append('Order ID: {} - {} from {}'.format(x, y, z))
        message = "\n".join(list)
        return message