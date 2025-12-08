import os


class Settings:
    def __init__(self):
        self.DATABASE_URL = self._get_database_url()

        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.STATIC_DIR = os.path.join(self.BASE_DIR, "static")
        self.TEMPLATES_DIR = os.path.join(self.BASE_DIR, "templates")

        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    def _get_database_url(self) -> str:
        db_url = os.getenv("DATABASE_URL")

        if not db_url:
            db_url = "postgresql://postgres:password@localhost:5432/item_gallery"
            print("Using default local database URL")
        else:
            print(f"Using database URL from environment")

        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        return db_url


settings = Settings()
