# botModel.py
import sqlite3


def get_bot_token():
    # Csatlakozás az adatbázishoz
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()

    # Lekérdezi az első bot token-t a bot táblából
    cursor.execute("SELECT bot_token FROM bot LIMIT 1")
    bot_token_record = cursor.fetchone()
    conn.close()

    if bot_token_record:
        return bot_token_record[0]
    else:
        raise ValueError("Nem található token az adatbázisban.")
