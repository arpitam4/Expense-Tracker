import pymysql as py
from datetime import datetime

class Database:
    def __init__(self, db):
        try:
            self.conn = py.connect(host='localhost', user='root', password='12345', database=db)
            self.cur = self.conn.cursor()
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS expense_record (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    item_name VARCHAR(255), 
                    item_price FLOAT, 
                    purchase_date DATE
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.conn = None

    def fetchRecord(self, query):
        if self.conn:
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows
        else:
            return []

    def insertRecord(self, item_name, item_price, purchase_date):
        if self.conn:
            try:
                # Convert date format to 'YYYY-MM-DD'
                purchase_date = datetime.strptime(purchase_date, '%d %B %Y').strftime('%Y-%m-%d')
                self.cur.execute("INSERT INTO expense_record (item_name, item_price, purchase_date) VALUES (%s, %s, %s)", (item_name, item_price, purchase_date))
                self.conn.commit()
            except Exception as e:
                print(f"Error inserting record: {e}")

    def removeRecord(self, rwid):
        if self.conn:
            self.cur.execute("DELETE FROM expense_record WHERE id=%s", (rwid,))
            self.conn.commit()

    def updateRecord(self, item_name, item_price, purchase_date, rid):
        if self.conn:
            try:
                # Convert date format to 'YYYY-MM-DD'
                purchase_date = datetime.strptime(purchase_date, '%d %B %Y').strftime('%Y-%m-%d')
                self.cur.execute("UPDATE expense_record SET item_name = %s, item_price = %s, purchase_date = %s WHERE id = %s", (item_name, item_price, purchase_date, rid))
                self.conn.commit()
            except Exception as e:
                print(f"Error updating record: {e}")

    def __del__(self):
        if self.conn:
            self.conn.close()
