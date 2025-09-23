def get_user_data():
    import sqlite3
    import os

    db_path = os.path.join("database", "user.db")

    if not os.path.exists(db_path):
        print("Database does not exist.")
        return {}
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='users';
    """)
    if cursor.fetchone() is None:
        print("Users table does not exist.")
        conn.close()
        return {}

    cursor.execute("SELECT username, password FROM users")
    rows = cursor.fetchall()
    conn.close()

    user_dict = {username: password for username, password in rows}
    return user_dict

