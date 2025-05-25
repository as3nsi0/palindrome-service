from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes import detection
from app.database import init_db
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Palindrome service")
    init_db()
    yield
    logger.info("Shutdown Palindrome service")

app = FastAPI(title="Palindrome Detection Service",
              lifespan=lifespan)
app.include_router(detection.router)