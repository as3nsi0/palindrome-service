from app.utils.logger_config import setup_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

logger = setup_logger(__name__)

def get_db():
    logger.info("Initializing DB")
    Base.metadata.create_all(bind=engine)

def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5433/detections")
    return database_url

try:
    db_url = get_database_url()
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base = declarative_base()
    logger.info("The connection to the DB was properly configured.")
except ValueError as e:
    logger.error(str(e))
    exit(1)