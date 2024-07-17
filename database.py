import sqlite3

import config


def create_database():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS users_data (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            username TEXT,
            GPT_35 INTEGER DEFAULT 0,
            GPT_4o INTEGER DEFAULT 0,
            ChatGPT_Flash INTEGER DEFAULT 0,
            ChatGPT_Pro INTEGER DEFAULT 0,
            DALLE3 INTEGER DEFAULT 0,
            premium_status TEXT DEFAULT 'NO',
            start_premium TEXT DEFAULT NULL,
            end_premium TEXT DEFAULT NULL,
            balance INTEGER DEFAULT 0,
            CURRENT_MODEL TEXT DEFAULT 'GPT 3.5',
            GPT_35_pd INTEGER DEFAULT {config.ChatGPT_35_free_per_day},
            GPT_4o_pd INTEGER DEFAULT {config.ChatGPT_4o_free_per_day},
            ChatGPT_Flash_pd INTEGER DEFAULT {config.Gemini_Flash_free_per_day},
            ChatGPT_Pro_pd INTEGER DEFAULT {config.Gemini_Pro_free_per_day},
            DALLE3_pd INTEGER DEFAULT {config.DALLE3_free_per_day},
            count_of_all_request INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


class Database:
    def __init__(self, db_name='user_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def insert_user(self, user_id, username):
        query = """INSERT INTO users_data (user_id, username) VALUES (?, ?)"""
        self.cursor.execute(query, (user_id, username,))
        self.conn.commit()

    def update_balance(self, user_id, balance):
        query = """UPDATE users_data SET balance = ? WHERE user_id = ?"""
        self.cursor.execute(query, (balance, user_id))
        self.conn.commit()

    def get_user_balance(self, user_id):
        query = """SELECT balance FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_premium_status(self, user_id):
        query = """SELECT premium_status FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def update_premium_status(self, user_id, premium_status):
        query = """UPDATE users_data SET premium_status = ? WHERE user_id = ?"""
        self.cursor.execute(query, (premium_status, user_id))
        self.conn.commit()

    def get_GPT_35(self, user_id):
        query = """SELECT GPT_35 FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_GPT_4o(self, user_id):
        query = """SELECT GPT_4o FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_Gemini_Flash(self, user_id):
        query = """SELECT ChatGPT_Flash FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_Gemini_Pro(self, user_id):
        query = """SELECT ChatGPT_Pro FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def update_GPT_35(self, user_id, GPT_35):
        query = """UPDATE users_data SET GPT_35 = ? WHERE user_id = ?"""
        self.cursor.execute(query, (GPT_35, user_id))
        self.conn.commit()

    def update_GPT_4o(self, user_id, GPT_4o):
        query = """UPDATE users_data SET GPT_4o = ? WHERE user_id = ?"""
        self.cursor.execute(query, (GPT_4o, user_id))
        self.conn.commit()

    def update_Gemini_Flash(self, user_id, ChatGPT_Flash):
        query = """UPDATE users_data SET ChatGPT_Flash = ? WHERE user_id = ?"""
        self.cursor.execute(query, (ChatGPT_Flash, user_id))
        self.conn.commit()

    def update_Gemini_Pro(self, user_id, ChatGPT_Pro):
        query = """UPDATE users_data SET ChatGPT_Pro = ? WHERE user_id = ?"""
        self.cursor.execute(query, (ChatGPT_Pro, user_id))
        self.conn.commit()

    def get_current_model(self, user_id):
        query = """SELECT CURRENT_MODEL FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def update_current_model(self, user_id, CURRENT_MODEL):
        query = """UPDATE users_data SET CURRENT_MODEL = ? WHERE user_id = ?"""
        self.cursor.execute(query, (CURRENT_MODEL, user_id))
        self.conn.commit()

    def get_all_ids(self):
        query = """SELECT user_id FROM users_data"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_ChatGPT_35_per_day(self, user_id):
        query = """SELECT GPT_35_pd FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_ChatGPT_4o_per_day(self, user_id):
        query = """SELECT GPT_4o_pd FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_Gemini_Pro_per_day(self, user_id):
        query = """SELECT ChatGPT_Pro_pd FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_Gemini_Flash_per_day(self, user_id):
        query = """SELECT ChatGPT_Flash_pd FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def update_ChatGPT_35_per_day(self, user_id, ChatGPT_35):
        query = """UPDATE users_data SET GPT_35_pd = ? WHERE user_id = ?"""
        self.cursor.execute(query, (ChatGPT_35, user_id))
        self.conn.commit()

    def update_ChatGPT_4o_per_day(self, user_id, ChatGPT_4o):
        query = """UPDATE users_data SET GPT_4o_pd = ? WHERE user_id = ?"""
        self.cursor.execute(query, (ChatGPT_4o, user_id))
        self.conn.commit()

    def update_Gemini_Flash_per_day(self, user_id, ChatGPT_Flash):
        query = """UPDATE users_data SET ChatGPT_Flash_pd = ? WHERE user_id = ?"""
        self.cursor.execute(query, (ChatGPT_Flash, user_id))
        self.conn.commit()

    def update_Gemini_Pro_per_day(self, user_id, ChatGPT_Pro_per_day):
        query = """UPDATE users_data SET ChatGPT_Pro_pd = ? WHERE user_id = ?"""
        self.cursor.execute(query, (ChatGPT_Pro_per_day, user_id))
        self.conn.commit()

    def get_DALLE3_per_day(self, user_id):
        query = """SELECT DALLE3_pd FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def update_dalle3_per_day(self, user_id, DALLE3_pd):
        query = """UPDATE users_data SET DALLE3_pd = ? WHERE user_id = ?"""
        self.cursor.execute(query, (DALLE3_pd, user_id))
        self.conn.commit()

    def get_DALLE3(self, user_id):
        query = """SELECT DALLE3 FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def update_dalle3(self, user_id, DALLE3):
        query = """UPDATE users_data SET DALLE3 = ? WHERE user_id = ?"""
        self.cursor.execute(query, (DALLE3, user_id))
        self.conn.commit()

    def update_balance_by_username(self, username, balance):
        query = """UPDATE users_data SET balance = ? WHERE username = ?"""
        self.cursor.execute(query, (balance, username))
        self.conn.commit()

    def update_prime_status_by_username(self, username, status):
        query = """UPDATE users_data SET status = ? WHERE username = ?"""
        self.cursor.execute(query, (status, username))
        self.conn.commit()

    def get_count_of_all_requests(self, user_id):
        query = """SELECT count_of_all_request FROM users_data WHERE user_id = ?"""
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def update_count_of_all_requests(self, user_id, count):
        query = """UPDATE users_data SET count_of_all_request = ? WHERE user_id = ?"""
        self.cursor.execute(query, (count, user_id))
        self.conn.commit()


create_database()
