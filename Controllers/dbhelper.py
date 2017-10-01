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
        #itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        #ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        #self.conn.execute(itemidx)
        #self.conn.execute(ownidx)
        self.conn.commit()

    def add_order(self, chat_id, location, food, userlocation, time, rcv_username):
        stmt = "INSERT INTO orders (chat_id, location, food, user_location, time, receiver_username, status) VALUES (?, ?, ?, ?, ?, ?, ?)"
        args = (chat_id, location, food, userlocation, time, rcv_username, 0)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_order(self, chat_id, location, food):
        stmt = "DELETE FROM orders WHERE chat_id = (?) AND location = (?) AND food = (?)"
        args = (chat_id, location, food)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_order(self, chat_id):
        stmt = "SELECT order_id, location, food,  time, user_location  FROM orders WHERE chat_id = (?)"
        args = (chat_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def get_all_orders(self):
        stmt = "SELECT order_id,  food, location,  time, user_location FROM orders WHERE status = 0"
        result = (x for x in self.conn.execute(stmt))
        self.conn.commit()
        return result

    def getOrderByOrderID(self, order_id):
        stmt = "SELECT order_id, food, location, time,user_location  FROM orders where order_id = (?)"
        args = (order_id,)
        result = (x for x in self.conn.execute(stmt, args))
        self.conn.commit()
        return result

    def bindSenderToOrder(self, sender_username, order_id):
        stmt = "UPDATE orders SET sender_username = (?) where order_id = (?)"
        args = (sender_username, order_id)
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

    def setStatus(self, status, order_id):
        stmt = "UPDATE orders SET status = (?) where order_id = (?)"
        args = (status, order_id)
        self.conn.execute(stmt, args)
        self.conn.commit()