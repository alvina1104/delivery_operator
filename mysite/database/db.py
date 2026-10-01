<<<<<<< HEAD
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

DB_URL = 'sqlite:///./data.db'
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
=======
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
>>>>>>> 79752a4 (chain)
