import os
from typing import Optional


class Settings:
    """Настройки приложения"""

    def __init__(self):
        # База данных
        self.DATABASE_URL = self._get_database_url()

        # Пути
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.STATIC_DIR = os.path.join(self.BASE_DIR, "static")
        self.TEMPLATES_DIR = os.path.join(self.BASE_DIR, "templates")

        # Настройки приложения
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"

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