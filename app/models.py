from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from config import DATABASE_URL, DB_TYPE

Base = declarative_base()


def connect_db():
    """Подключение к БД"""
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())
    return session


def create_tables():
    """Создание таблиц"""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print(f"Tables created for {DB_TYPE}")


def create_database_if_not_exists():
    """Создать базу данных если нужно (для PostgreSQL обычно уже создана)"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("Database tables ready")
    except Exception as e:
        print(f"Database error: {e}")


class User(Base):
    __tablename__ = 'users_app'

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    first_name = Column(String(256))
    last_name = Column(String(256))
    nick_name = Column(String(256))
    created_at = Column(String(256), default=datetime.utcnow().isoformat())


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users_app.id'))
    title = Column(String(256), nullable=False)
    description = Column(Text)
    cover_image = Column(String(512))  # URL или путь к титульной картинке
    images = Column(Text)  # JSON список картинок
    created_at = Column(String(256), default=datetime.utcnow().isoformat())


class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True)
    token = Column(String(64), nullable=False, unique=True)  # Укороченный токен
    user_id = Column(Integer, ForeignKey('users_app.id'))
    created_at = Column(String(256), default=datetime.utcnow().isoformat())

    @staticmethod
    def generate_token():
        """Генерация простого токена"""
        return secrets.token_urlsafe(32)  # 32 байта в URL-safe формате
