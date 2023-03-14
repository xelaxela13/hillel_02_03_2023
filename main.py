import os
import sqlite3


class DB:

    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = sqlite3.connect(os.path.join(os.getcwd(), 'new.db'))
        return self.db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()


if __name__ == '__main__':
    request = """CREATE TABLE IF NOT EXISTS 'users' (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name TEXT(255)
    )"""
    with DB() as cursor:
        try:
            res = cursor.execute(request).fetchall()
        except sqlite3.Error as err:
            print(err)
    print(res)
