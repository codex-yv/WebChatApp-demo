import sqlite3
import os

def get_all_chats():
    db_path = os.path.join("database", "chatHistory.db")
    conn = sqlite3.connect(db_path)
    
    cursor = conn.cursor()

    cursor.execute("SELECT username, data FROM community")
    rows = cursor.fetchall()

    conn.close()
    return rows
