import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Только Postgres для Render.com
DB_TYPE = 'postgresql'

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if not DATABASE_URL:
    DATABASE_URL = 'postgresql://user:password@localhost:5432/app_db'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
JS_DIR = os.path.join(STATIC_DIR, 'js')

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

print(f"📊 Database: {DB_TYPE}")
print(f"📁 Database URL configured")
print(f"📝 Templates dir: {TEMPLATES_DIR}")