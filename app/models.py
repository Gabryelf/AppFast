from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import secrets
import json

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")


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
    cover_image = Column(String(512))
    images = Column(Text, default='[]')  # JSON список
    created_at = Column(String(256), default=datetime.utcnow().isoformat())

    def get_images_list(self):
        """Получить список изображений"""
        if self.images:
            try:
                return json.loads(self.images)
            except:
                return []
        return []


class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True)
    token = Column(String(64), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users_app.id'))
    created_at = Column(String(256), default=datetime.utcnow().isoformat())

    @staticmethod
    def generate_token():
        """Генерация токена"""
        return secrets.token_urlsafe(32)
