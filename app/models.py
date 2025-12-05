from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime
from enum import Enum

from config import DATABASE_URL, DB_TYPE

Base = declarative_base()


class StreamStatus(Enum):
    PLANED = 'planed'
    ACTIVE = 'active'
    CLOSED = 'closed'


def connect_db():
    """Подключение к БД с автоматическим созданием базы если нужно"""
    if DB_TYPE == 'mysql':
        create_mysql_database_if_not_exists()

    if DB_TYPE == 'sqlite':
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(DATABASE_URL)

    session = Session(bind=engine.connect())
    return session


def create_mysql_database_if_not_exists():
    """Создать базу данных MySQL если она не существует"""
    try:
        from urllib.parse import urlparse

        parsed = urlparse(DATABASE_URL)
        db_name = parsed.path[1:]  # убираем первый слэш

        base_url = DATABASE_URL.replace(f'/{db_name}', '')

        temp_engine = create_engine(base_url)

        with temp_engine.connect() as conn:
            result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
            exists = result.fetchone() is not None

            if not exists:
                print(f"Creating MySQL database: {db_name}")
                conn.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                print(f"Database '{db_name}' created")
            else:
                print(f"Database '{db_name}' already exists")

    except Exception as e:
        print(f"Could not check/create database: {e}")


def create_tables():
    if DB_TYPE == 'sqlite':
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(bind=engine)
    print(f"Tables created for {DB_TYPE}")


class User(Base):
    __tablename__ = 'users_app'

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    first_name = Column(String(256))
    last_name = Column(String(256))
    nick_name = Column(String(256))
    created_at = Column(String(256), default=datetime.utcnow().isoformat())


class Stream(Base):
    __tablename__ = 'stream'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users_app.id'))
    title = Column(String(256))
    topic = Column(String(256))
    status = Column(String(50), default=StreamStatus.PLANED.value)
    created_at = Column(String(256), default=datetime.utcnow().isoformat())


class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True)
    token = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey('users_app.id'))
    created_at = Column(String(256), default=datetime.utcnow().isoformat())
