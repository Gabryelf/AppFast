from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from app.models import Base

from app.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())
    inspector = inspect(engine)

    existing_tables = inspector.get_table_names()

    if 'users' not in existing_tables:
        session.execute("""create table users (
               id integer not null primary key,
               email varchar(256),
               password varchar(256),
               first_name varchar(256),
               last_name varchar(256),
               nick_name varchar(256),
               created_at varchar(256)
               );""")

    if 'auth_token' not in existing_tables:
        session.execute("""create table auth_token (
              id integer not null primary key,
              token varchar(256),
              user_id integer references users,
              created_at varchar(256)
              );""")

    if 'stream' not in existing_tables:
        session.execute("""create table stream (
               id integer not null primary key,
               title varchar(256),
               topic varchar(256),
               status varchar(256),
               created_at varchar(256)
               );""")

    session.commit()
    session.close()


#if __name__ == '__main__':
    main()
#Base.metadata.create_all(engine)