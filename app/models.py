from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from app.database import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    language = Column(String, nullable=False, index=True)
    is_palindrome = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)