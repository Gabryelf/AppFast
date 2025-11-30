import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = 'app.db'

DB_PATH = os.path.join(BASE_DIR, DB_NAME)
DATABASE_URL = f'sqlite:///{DB_PATH}'

print(f"Database path: {DB_PATH}")
