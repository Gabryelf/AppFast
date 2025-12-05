import os
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Это AppFast/

DB_TYPE = 'mysql'

DB_NAME = 'app.db'
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

if DB_TYPE == 'sqlite':
    DATABASE_URL = f'sqlite:///{DB_PATH}'
elif DB_TYPE == 'postgresql':
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/app_db')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
elif DB_TYPE == 'mysql':
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')  # пароль, если установили при инсталляции
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DB = os.getenv('MYSQL_DATABASE', 'app_db')

    DATABASE_URL = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'

    if os.environ.get('MYSQL_URL'):
        DATABASE_URL = os.environ.get('MYSQL_URL')
else:
    raise ValueError(f"Unknown DB_TYPE: {DB_TYPE}. Use 'sqlite', 'postgresql' or 'mysql'")

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
JS_DIR = os.path.join(STATIC_DIR, 'js')

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

print(f"📊 Database: {DB_TYPE}")
print(f"📁 Database URL: {DATABASE_URL}")
print(f"📝 Templates dir: {TEMPLATES_DIR}")
