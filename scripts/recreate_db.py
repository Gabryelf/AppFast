import os
import sqlite3
from app.config import DB_PATH


def recreate_database():
    #if os.path.exists(DB_PATH):
        #os.remove(DB_PATH)
       # print(f"Removed old database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создаем таблицы
    cursor.execute("""
        CREATE TABLE users_app (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(256) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            first_name VARCHAR(256),
            last_name VARCHAR(256),
            nick_name VARCHAR(256),
            created_at VARCHAR(256)
        )
    """)

    cursor.execute("""
        CREATE TABLE auth_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token VARCHAR(256) NOT NULL,
            user_id INTEGER REFERENCES users_app(id),
            created_at VARCHAR(256)
        )
    """)

    cursor.execute("""
        CREATE TABLE stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users_app(id),
            title VARCHAR(256),
            topic VARCHAR(256),
            status VARCHAR(256),
            created_at VARCHAR(256)
        )
    """)

    conn.commit()
    conn.close()
    print(f"New database created: {DB_PATH}")


if __name__ == '__main__':
    recreate_database()