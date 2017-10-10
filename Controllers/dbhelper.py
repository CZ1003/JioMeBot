import sqlite3


class DBHelper:
    def __init__(self, dbname="dabao.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname,  check_same_thread = False)
        c = self.conn.cursor()

    def setup(self):
        tblstmt = """CREATE TABLE IF NOT EXISTS orders (
                    chat_id INTEGER, 
                    location TEXT, 
                    food TEXT)"""
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_order(self, chat_id, location, food, userlocation, time, rcv_username, tip):
        stmt = "INSERT INTO orders (chat_id, location, food, user_location, time, receiver_username, status, tip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        args = (chat_id, location, food, userlocation, time, rcv_username, 0, tip)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_order(self, chat_id, location, food):
        stmt = "DELETE FROM orders WHERE chat_id = (?) AND location = (?) AND food = (?)"
        args = (chat_id, location, food)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_order(self, chat_id):
        stmt = "SELECT order_id, location, food,  time, user_location, tip  FROM orders WHERE chat_id = (?)"
        args = (chat_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def get_all_orders(self):
        stmt = "SELECT chat_id, order_id,  food, location,  time, user_location, tip FROM orders WHERE status = 0"
        result = (x for x in self.conn.execute(stmt))
        self.conn.commit()
        return result

    def get_all_placedorderswithoutownorder(self, chatid):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip FROM orders WHERE NOT chat_id = (?) AND status = 0"
        args = (chatid,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def getAllPlacedOrdersByChatID(self, chatId, orderId):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip FROM orders WHERE status = 0 AND chat_id = (?) AND order_id = (?)"
        args = (chatId, orderId,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def get_all_pendingorders_by_chat_id(self, chat_id):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip, sender_username FROM orders WHERE status = 1 AND chat_id = (?)"
        args = (chat_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def get_unconfirmed_orders_by_chat_id(self, chat_id):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip FROM orders WHERE status = 0 AND chat_id = (?)"
        args = (chat_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def getOrderByOrderID(self, order_id):
        stmt = "SELECT order_id, food, location, time,user_location, tip  FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def getPendingOrderByOrderID(self, order_id, username):
        stmt = "SELECT order_id, food, location, time,user_location, tip  FROM orders where order_id = (?) AND sender_username = (?) AND status = 1"
        args = (order_id, username)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def getPendingOrdersByUsername(self, username):
        stmt = "SELECT order_id, food, location, time,user_location, tip, receiver_username  FROM orders where sender_username = (?) AND status = 1"
        args = (username,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def bindSenderToOrder(self, sender_username, sender_chatid, order_id):
        stmt = "UPDATE orders SET sender_username = (?), sender_chatid = (?) where order_id = (?)"
        args = (sender_username, sender_chatid, order_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def getChatIdByOrderId(self, order_id):
        stmt = "SELECT chat_id, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def getUsernameByOrderId(self, order_id):
        stmt = "SELECT receiver_username, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def getsenderByOrderId(self, order_id):
        stmt = "SELECT sender_username, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def getSenderChatIDbyOrderId(self, order_id):
        stmt = "SELECT sender_chatid, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def removeExpiredOrders(self, datetime):
        stmt = "DELETE FROM orders WHERE time = (?)"
        args = (datetime,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def removePlacedOrder(self, order_id):
        stmt = "DELETE FROM orders WHERE order_id = (?) and status = 0"
        args = (order_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    ## To be done
    def checkNumOfOrders(self, chatid):
        stmt = "SELECT * FROM orders WHERE chat_id = (?)"
        args = (chatid,)
        count = self.conn.execute(stmt, args)
        self.conn.commit()
        return count

    # 0 - Available
    # 1 - Pending order
    # 2 - Delivered
    # 3 - Cancelled
    def setStatus(self, status, order_id):
        stmt = "UPDATE orders SET status = (?) where order_id = (?)"
        args = (status, order_id)
        self.conn.execute(stmt, args)
        self.conn.commit()