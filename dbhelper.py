import sqlite3


class DBHelper:
    def __init__(self, dbname="dabao.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
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

    def add_order(self, chat_id, location, food):
        stmt = "INSERT INTO orders (chat_id, location, food) VALUES (?, ?, ?)"
        args = (chat_id, location, food)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_order(self, chat_id, location, food):
        stmt = "DELETE FROM orders WHERE chat_id = (?) AND location = (?) AND food = (?)"
        args = (chat_id, location, food)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_order(self, chat_id):
        stmt = "SELECT food, location FROM orders WHERE chat_id = (?)"
        args = (chat_id,)
        return [x for x in self.conn.execute(stmt, args)]

    def get_all_orders(self):
        stmt = "SELECT food, location FROM orders"
        return [x for x in self.conn.execute(stmt)]