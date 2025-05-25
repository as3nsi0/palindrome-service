from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app import palindrome, schemas, models

def create_detection(detection: schemas.Palindrome,
                     db: Session) -> schemas.Detection:
    is_palindrome = palindrome.is_palindrome(detection.text)
    detection = models.Detection(
        text=detection.text,
        language=detection.language,
        is_palindrome=is_palindrome
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection


def list_detections(language: Optional[str],
                    start_date: Optional[datetime],
                    end_date: Optional[datetime],
                    db: Session) -> List[schemas.Detection]:
    query = db.query(models.Detection)
    if language:
        query = query.filter(models.Detection.language == language)
    if start_date:
        query = query.filter(models.Detection.created_at >= start_date)
    if end_date:
        query = query.filter(models.Detection.created_at <= end_date)
    return query.order_by(models.Detection.created_at.desc()).all()

def find_specific_detection(detection_id: int,
                            db: Session) -> schemas.Detection:
    return db.query(models.Detection).filter(models.Detection.id == detection_id).first()

def delete_detection(detection_id: int,
                     db: Session):
    def __get_detection_by_id(db: Session, detection_id:int):
        return db.query(models.Detection).filter(models.Detection.id == detection_id).first()

    detection = __get_detection_by_id(db=db,
                                      detection_id=detection_id)
    if not detection:
        return None

    db.delete(detection)
    db.commit()