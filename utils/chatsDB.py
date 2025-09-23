import sqlite3
import os

async def create_chat_history_db():
    folder = "database"
    db_path = os.path.join(folder, "chatHistory.db")

    if not os.path.exists(folder):
        os.makedirs(folder)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community (
            username TEXT,
            data TEXT
        )
    """)

    conn.commit()
    conn.close()

