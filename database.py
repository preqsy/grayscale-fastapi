from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/dbname" #use your db url here
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
