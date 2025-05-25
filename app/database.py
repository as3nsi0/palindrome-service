from app.utils.logger_config import setup_logger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

logger = setup_logger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/detections")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def init_db():
    logger.info("Initializing DB")
    Base.metadata.create_all(bind=engine)