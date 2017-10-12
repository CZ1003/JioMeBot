import sqlite3

## Database Class (Data Access Layer)

class DBHelper:
    # Initiating of database
    def __init__(self, dbname="dabao.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname,  check_same_thread = False)
        c = self.conn.cursor()

        #Adds order into database
    def add_order(self, chat_id, location, food, userlocation, time, rcv_username, tip):
        stmt = "INSERT INTO orders (chat_id, location, food, user_location, time, receiver_username, status, tip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        args = (chat_id, location, food, userlocation, time, rcv_username, 0, tip)
        self.conn.execute(stmt, args)
        self.conn.commit()
        #Deletes order from database
    def delete_order(self, chat_id, location, food):
        stmt = "DELETE FROM orders WHERE chat_id = (?) AND location = (?) AND food = (?)"
        args = (chat_id, location, food)
        self.conn.execute(stmt, args)
        self.conn.commit()
        #Retrieves order
    def get_order(self, chat_id):
        stmt = "SELECT order_id, location, food,  time, user_location, tip  FROM orders WHERE chat_id = (?)"
        args = (chat_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves all placed orders (Orders not accepted)
    def get_all_orders(self):
        stmt = "SELECT chat_id, order_id,  food, location,  time, user_location, tip FROM orders WHERE status = 0"
        result = (x for x in self.conn.execute(stmt))
        self.conn.commit()
        return result
        #Retrieves order to remove when expires
    def get_all_orders_for_expiry(self):
        stmt = "SELECT chat_id, order_id,  food, location, time, user_location, status, tip, sender_chatid FROM orders WHERE status = 0 OR status = 1 "
        result = (x for x in self.conn.execute(stmt))
        self.conn.commit()
        return result
        #Retrieves all placed orders without own order visible
    def get_all_placedorderswithoutownorder(self, chatid):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip FROM orders WHERE NOT chat_id = (?) AND status = 0"
        args = (chatid,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves all placed orders by chat ID (For personal use)
    def getAllPlacedOrdersByChatID(self, chatId, orderId):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip FROM orders WHERE status = 0 AND chat_id = (?) AND order_id = (?)"
        args = (chatId, orderId,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves all pending orders by chat ID
    def get_all_pendingorders_by_chat_id(self, chat_id):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip, sender_username FROM orders WHERE status = 1 AND chat_id = (?)"
        args = (chat_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieve unconfirmed orders by chat id
    def get_unconfirmed_orders_by_chat_id(self, chat_id):
        stmt = "SELECT order_id,  food, location,  time, user_location, tip FROM orders WHERE status = 0 AND chat_id = (?)"
        args = (chat_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves order by Order ID
    def getOrderByOrderID(self, order_id):
        stmt = "SELECT order_id, food, location, time,user_location, tip  FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves pending order by Order ID
    def getPendingOrderByOrderID(self, order_id, username):
        stmt = "SELECT order_id, food, location, time,user_location, tip  FROM orders where order_id = (?) AND sender_username = (?) AND status = 1"
        args = (order_id, username)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves pending order by User Name
    def getPendingOrdersByUsername(self, username):
        stmt = "SELECT order_id, food, location, time,user_location, tip, receiver_username  FROM orders where sender_username = (?) AND status = 1"
        args = (username,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

     # Retrieves pending order by username to remove
    def getPendingOrdersByUsernameForRemoval(self, username):
        stmt = "SELECT chat_id, order_id, food, location, time,user_location, tip, receiver_username  FROM orders where sender_username = (?) AND status = 1"
        args = (username,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Updates sender_id of the order
    def bindSenderToOrder(self, sender_username, sender_chatid, order_id):
        stmt = "UPDATE orders SET sender_username = (?), sender_chatid = (?) where order_id = (?)"
        args = (sender_username, sender_chatid, order_id)
        self.conn.execute(stmt, args)
        self.conn.commit()
        #Retrieves chatID from order ID to send message to
    def getChatIdByOrderId(self, order_id):
        stmt = "SELECT chat_id, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves username by order ID
    def getUsernameByOrderId(self, order_id):
        stmt = "SELECT receiver_username, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves sender's username by Order ID
    def getsenderByOrderId(self, order_id):
        stmt = "SELECT sender_username, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Retrieves sender's chat ID by Order ID
    def getSenderChatIDbyOrderId(self, order_id):
        stmt = "SELECT sender_chatid, food FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result
        #Deletes expired orders
    def removeExpiredOrders(self, datetime):
        stmt = "DELETE FROM orders WHERE time = (?)"
        args = (datetime,)
        self.conn.execute(stmt, args)
        self.conn.commit()
        #removes placed orders for customer
    def removePlacedOrder(self, order_id):
        stmt = "DELETE FROM orders WHERE order_id = (?) and status = 0"
        args = (order_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

        #updates status between placed and pending.
    def setStatus(self, status, order_id):
        stmt = "UPDATE orders SET status = (?) where order_id = (?)"
        args = (status, order_id)
        self.conn.execute(stmt, args)
        self.conn.commit()