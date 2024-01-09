# botModel.py
import base64
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
        # Dekódolja a token-t Base64 kódolásból
        decoded_bytes = base64.b64decode(bot_token_record[0])
        decoded_token = decoded_bytes.decode('utf-8')
        return decoded_token
    else:
        raise ValueError("Nem található token az adatbázisban.")
