import os

# Определяем корневую директорию проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Это AppFast/

# Пути к файлам и папкам
DB_NAME = 'app.db'
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
DATABASE_URL = f'sqlite:///{DB_PATH}'

# Пути к шаблонам и статическим файлам
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
JS_DIR = os.path.join(STATIC_DIR, 'js')

# Проверяем существование папок
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

print(f"Project root: {BASE_DIR}")
print(f"Database path: {DB_PATH}")
print(f"Templates dir: {TEMPLATES_DIR}")
print(f"Static dir: {STATIC_DIR}")
