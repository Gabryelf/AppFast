from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import secrets
import json

from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


class User(Base):
    __tablename__ = "users_app"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    nick_name = Column(String(100))
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    items = relationship("Item", back_populates="author", cascade="all, delete-orphan")
    tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_app.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    cover_image = Column(String(500))
    images = Column(Text, default="[]")
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    author = relationship("User", back_populates="items")

    @property
    def images_list(self) -> list:
        """Получить список изображений как Python список"""
        try:
            return json.loads(self.images) if self.images else []
        except json.JSONDecodeError:
            return []


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users_app.id"), nullable=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    user = relationship("User", back_populates="tokens")

    @staticmethod
    def generate_token() -> str:
        """Генерация нового токена"""
        return secrets.token_urlsafe(32)
