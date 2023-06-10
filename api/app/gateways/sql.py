import sqlite3
from api.app.utils.logging import APILogger


class SQLManager:
    def __init__(self):
        self.sqlite_dir = './app/data'
        self.sqlite_db_path = self.sqlite_dir + '/users.db'

    def get_user(self, username):
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=?"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()

        return user
