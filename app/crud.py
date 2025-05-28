from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session

from app import palindrome, schemas, models

from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

def create_detection(detection_create: schemas.DetectionCreate,
                     db: Session) -> models.Detection:
    is_palindrome = palindrome.is_palindrome(detection_create.text)
    detection = models.Detection(
        text=detection_create.text,
        language=detection_create.language,
        is_palindrome=is_palindrome,
        created_at=datetime.now(timezone.utc)
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    logger.info(f"The palindrome was inserted to the DB: [Text: {detection.text}], [Language: {detection.language}]")
    return detection


def list_detections(language: Optional[str],
                    start_date: Optional[datetime],
                    end_date: Optional[datetime],
                    db: Session) -> List[Optional[models.Detection]]:

    query = db.query(models.Detection)
    if language:
        query = query.filter(models.Detection.language == language)
    if start_date:
        query = query.filter(models.Detection.created_at >= start_date)
    if end_date:
        query = query.filter(models.Detection.created_at <= end_date)
    return query.order_by(models.Detection.created_at.desc()).all()

def find_specific_detection(detection_id: int,
                            db: Session) -> Optional[models.Detection]:
    return db.query(models.Detection).filter(models.Detection.id == detection_id).first()

def delete_detection(detection_id: int,
                     db: Session) -> Optional[models.Detection]:
    def __get_detection_by_id(db: Session, detection_id: int) -> models.Detection:
        return db.query(models.Detection).filter(models.Detection.id == detection_id).first()

    detection = __get_detection_by_id(db=db,
                                      detection_id=detection_id)
    if not detection:
        return None

    db.delete(detection)
    db.commit()
    return detection