import os
import sqlite3

async def create_user_db():
    folder = "database"
    db_path = os.path.join(folder, "user.db")

    if not os.path.exists(folder):
        os.makedirs(folder)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    print(f"Database created at {db_path} with 'users' table.")
