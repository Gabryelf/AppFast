import os


class Settings:
    """Настройки приложения"""

    def __init__(self):
        # База данных
        self.DATABASE_URL = self._get_database_url()

        # Пути - корневая директория проекта
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.STATIC_DIR = os.path.join(self.BASE_DIR, "static")  # Корневой static
        self.TEMPLATES_DIR = os.path.join(self.BASE_DIR, "templates")  # Корневой templates

        # Настройки приложения
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"

        # Проверяем существование директорий
        self._check_directories()

    def _check_directories(self):
        """Проверяем существование необходимых директорий"""
        if not os.path.exists(self.STATIC_DIR):
            print(f"⚠️ Static directory not found: {self.STATIC_DIR}")
            os.makedirs(self.STATIC_DIR, exist_ok=True)
            print(f"✅ Created static directory: {self.STATIC_DIR}")

        if not os.path.exists(self.TEMPLATES_DIR):
            print(f"⚠️ Templates directory not found: {self.TEMPLATES_DIR}")
            os.makedirs(self.TEMPLATES_DIR, exist_ok=True)
            print(f"✅ Created templates directory: {self.TEMPLATES_DIR}")

    def _get_database_url(self) -> str:
        """Получение URL базы данных"""
        # 1. Проверяем переменную окружения Render
        db_url = os.getenv("DATABASE_URL")

        # 2. Если нет - используем локальную базу по умолчанию
        if not db_url:
            db_url = "postgresql://postgres:password@localhost:5432/item_gallery"
            print("⚠️ Using default local database URL")
        else:
            print(f"✅ Using database URL from environment")

        # Исправляем URL для совместимости
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        return db_url


# Создаем экземпляр настроек
settings = Settings()