import sqlite3
import os

def add_user(username, password):
    db_path = os.path.join("database", "user.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()