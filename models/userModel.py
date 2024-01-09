# userModel.py

import sqlite3

'''
Létrehoz egy kapcsolatot egy SQLite adatbázissal
'''


def create_connection():
    return sqlite3.connect("db/users.db")


'''
Ellenőrzi, hogy létezik-e egy adott felhasználó az adatbázisban
'''


def user_exists(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone() is not None


'''
Egy új felhasználót hoz létre az adatbázisban
'''


def create_user(conn, name, user_id, channel_id):
    query = """
    INSERT INTO users (name, user_id, channel_id, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """
    with conn:
        conn.execute(query, (name, user_id, channel_id))


'''
Egy adott felhasználó adatait kéri le az adatbázisból
'''


def fetch_user(conn, user_id):
    query = """
    SELECT * FROM users WHERE user_id = ?
    """
    with conn:
        return conn.execute(query, (user_id,)).fetchone()
