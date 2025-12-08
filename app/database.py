from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import secrets
import json
import os

from app.config import settings

# Создаем engine с параметрами по умолчанию
Base = declarative_base()
engine = None
SessionLocal = None


def init_database():
    """Инициализация подключения к базе данных"""
    global engine, SessionLocal

    if engine is None:
        try:
            print(f"🔗 Connecting to database...")
            print(f"   URL: {settings.DATABASE_URL[:50]}...")

            engine = create_engine(
                settings.DATABASE_URL,
                echo=settings.DEBUG,
                pool_pre_ping=True,
                pool_recycle=300
            )

            SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
                expire_on_commit=False
            )

            return True
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            return False

    return True


def get_db() -> Session:
    """Dependency для получения сессии базы данных"""
    if SessionLocal is None:
        init_database()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Создание таблиц в базе данных"""
    if not init_database():
        print("⚠️ Skipping table creation due to connection issues")
        return False

    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


class User(Base):
    __tablename__ = "users_app"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    nick_name = Column(String(100))
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_app.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    cover_image = Column(String(500))
    images = Column(Text, default="[]")
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users_app.id"), nullable=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    @staticmethod
    def generate_token() -> str:
        """Генерация нового токена"""
        return secrets.token_urlsafe(32)
