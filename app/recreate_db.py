import os
import sys
import sqlite3
from app.config import DB_PATH, DB_TYPE, DATABASE_URL


def recreate_database():
    """Пересоздать базу данных"""
    print(f"Recreating {DB_TYPE} database...")
    print(f"Using URL: {DATABASE_URL}")

    if DB_TYPE == 'sqlite':
        recreate_sqlite()
    elif DB_TYPE == 'postgresql':
        recreate_postgresql()
    elif DB_TYPE == 'mysql':
        recreate_mysql()
    else:
        print(f"Unknown DB_TYPE: {DB_TYPE}")


def recreate_sqlite():
    """Пересоздать SQLite базу"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed old database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
    print(f"New SQLite database created: {DB_PATH}")


def recreate_postgresql():
    """Создать таблицы в PostgreSQL"""
    try:
        from sqlalchemy import create_engine
        print("Connecting to PostgreSQL...")

        engine = create_engine(DATABASE_URL)
        from app.models import Base
        Base.metadata.create_all(bind=engine)

        print("PostgreSQL tables created successfully")

    except Exception as e:
        print(f"Error: {e}")


def recreate_mysql():
    """Создать таблицы в MySQL с проверкой"""
    try:
        from sqlalchemy import create_engine, text

        print("Testing MySQL connection...")

        parsed_url = DATABASE_URL
        if 'mysql' in parsed_url:
            engine = create_engine(parsed_url)

            with engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"Connected to MySQL Server {version}")

            # Создаем таблицы
            from app.models import Base
            Base.metadata.create_all(bind=engine)

            print("MySQL tables created successfully")

            # Проверяем таблицы
            with engine.connect() as conn:
                result = conn.execute(text("SHOW TABLES"))
                tables = result.fetchall()
                print(f"Tables in database: {[table[0] for table in tables]}")

        else:
            print("Invalid MySQL URL format")

    except Exception as e:
        print(f"Error: {e}")


def check_mysql_connection():
    """Проверить подключение к MySQL"""
    try:
        from sqlalchemy import create_engine, text
        import urllib.parse

        parsed = urllib.parse.urlparse(DATABASE_URL)

        print(f"  Host: {parsed.hostname}")
        print(f"  Port: {parsed.port}")
        print(f"  Database: {parsed.path[1:]}")
        print(f"  User: {parsed.username}")

        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Connection successful!")
            return True

    except Exception as e:
        print(f"Connection failed: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check_mysql_connection()
    else:
        recreate_database()
