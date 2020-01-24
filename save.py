import sqlite3

class Savebase:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS saved (setname TEXT, items TEXT, quantity INTEGER, price INTEGER, total TEXT, summing INTEGER)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM saved")
        rows = self.cur.fetchall()
        return rows

    def insert(self, setname, items, quantity, price, total, summing):
        self.cur.execute("INSERT INTO saved VALUES (?, ?, ?, ?, ?, ?)", (setname, items, quantity, price, total, summing,))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM saved WHERE id=?", (id,))
        self.conn.commit()

    def read_from_db(self, setname):
        self.cur.execute("SELECT * FROM saved WHERE setname=?", (setname,))
        sums = self.cur.fetchall()
        return sums

    def read_total_db(self, setname):
        self.cur.execute("SELECT SUM(summing) FROM saved WHERE setname=?", (setname,))
        sums = self.cur.fetchall()
        return sums

    # def update(self, id, items, quantity, price, total):
    #     self.cur.execute("UPDATE list SET items = ?, quantity = ?, price = ?, total = ? WHERE id = ?",
    #                         (items, quantity, price, total, id))
    #     self.conn.commit()

    def __del__(self):
        self.conn.close()

