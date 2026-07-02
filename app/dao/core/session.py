from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
