import sqlite3
from app.logging import logging


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

    def get_user_basics(self, username):
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=?"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        fornec_id = user[1]
        username = user[2]
        razao_social = user[4]
        plano = user[5]
        conn.close()

        json_data = {
            "fornecId": fornec_id,
            "username": username,
            "razaoSocial": razao_social,
            "plano": plano,
        }

        return json_data

    def create_user(self, fornec_id, username, hashed_password, fornec_razao_social, fornec_plano):
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=?"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Logging the registration error
            logging.info(
                f"Registration error: Username '{username}' already exists")
            return

        query = "INSERT INTO users (fornec_id, username, password, razao_social, plano) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query,
                       (fornec_id, username, hashed_password, fornec_razao_social, fornec_plano))
        conn.close()
