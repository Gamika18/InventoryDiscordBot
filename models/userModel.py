# database_queries.py

import sqlite3

def create_connection():
    return sqlite3.connect("db/users.db")

def user_exists(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone() is not None


def create_user(conn, name, user_id, channel_id):
    query = """
    INSERT INTO users (name, user_id, channel_id) VALUES (?, ?, ?)
    """
    with conn:
        conn.execute(query, (name, user_id, channel_id))

def fetch_user(conn, user_id):
    query = """
    SELECT * FROM users WHERE user_id = ?
    """
    with conn:
        return conn.execute(query, (user_id,)).fetchone()
