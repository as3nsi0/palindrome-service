from app.utils import logger_config

from datetime import datetime
from http.client import HTTPException
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas, palindrome, database, models

logger = logger_config.setup_logger(__name__)

router = APIRouter(prefix="/detections", tags=["Detections"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Detection)
def create_detection(detection: schemas.Palindrome, db: Session = Depends(get_db)):
    is_palindrome = palindrome.is_palindrome(detection.text)
    detection = models.Detection(
        text = detection.text,
        language = detection.language,
        is_palindrome = is_palindrome
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection

@router.get("/", response_model=List[schemas.Detection])
def list_detections(language: Optional[str] = Query(default=None,
                                                    description="Filter by language",
                                                    example="Spanish"),
                    start_date: Optional[datetime] = Query(default=None,
                                                           description="Filter by language (ISO 8601)",
                                                           example="2025-05-23T16:11:54"),
                    end_date: Optional[datetime] = Query(default=None,
                                                         description="Filter to date (ISO 8601)",
                                                         example="2025-05-26T16:11:54"),
                    db: Session = Depends(get_db)):

    query = db.query(models.Detection)
    if language and language.isalpha():
        query = query.filter(models.Detection.language == language)
    if start_date:
        query = query.filter(models.Detection.created_at >= start_date)
    if end_date:
        query = query.filter(models.Detection.created_at <= end_date)
    return query.order_by(models.Detection.created_at.desc()).all()

@router.get("/{detection_id}", response_model=schemas.Detection)
def find_specific_detection(detection_id: int,
                            db: Session = Depends(get_db)):
    detection = db.query(models.Detection).filter(models.Detection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection

@router.delete("/{detection_id}", response_model=schemas.Detection)
def delete_detection(detection_id: int, db: Session = Depends(get_db)):
    def __get_detection_by_id(db: Session, detection_id:int):
        return db.query(models.Detection).filter(models.Detection.id == detection_id).first()

    detection = __get_detection_by_id(db=db,
                                      detection_id=detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    db.delete(detection)
    db.commit()
    return detection
