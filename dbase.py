import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS list (items TEXT, quantity INTEGER, price INTEGER, total TEXT, summing INTEGER)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM list")
        rows = self.cur.fetchall()
        return rows

    def insert(self, items, quantity, price, total, summing):
        self.cur.execute("INSERT INTO list VALUES (?, ?, ?, ?, ?)", (items, quantity, price, total, summing))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM list WHERE id=?", (id,))
        self.conn.commit()

    def read_from_db(self):
        self.cur.execute("SELECT SUM(summing) FROM list")
        sums = self.cur.fetchall()
        return sums

    def update(self, id, items, quantity, price, total):
        self.cur.execute("UPDATE list SET items = ?, quantity = ?, price = ?, total = ? WHERE id = ?",
                            (items, quantity, price, total, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

