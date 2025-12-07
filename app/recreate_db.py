import sys
from sqlalchemy import create_engine, text
from app.models import Base, DATABASE_URL


def recreate_database():
    """Создаем таблицы в PostgreSQL"""
    try:
        print(f"Connecting to PostgreSQL at {DATABASE_URL}")
        engine = create_engine(DATABASE_URL)

        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        print("PostgreSQL tables created successfully")

        # Проверяем таблицы
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"Tables in database: {', '.join(tables)}")

    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


def check_database_connection():
    """Проверяем подключение к базе данных"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check_database_connection()
    else:
        recreate_database()
