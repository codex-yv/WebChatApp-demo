import sqlite3
import os

async def insert_chat(username, data):
    db_path = os.path.join("database", "chatHistory.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO community (username, data) VALUES (?, ?)", (username, data))

    conn.commit()
    conn.close()
