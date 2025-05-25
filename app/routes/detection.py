from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import schemas, palindrome, database
from app.models import Detection

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
    detection = Detection(
        text = detection.text,
        language = detection.language,
        is_palindrome = is_palindrome
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection

@router.get("/", response_model=list[schemas.Detection])
def get_all_detections(db: Session = Depends(get_db)):
    result = db.execute(select(Detection))
    return result.scalars().all()