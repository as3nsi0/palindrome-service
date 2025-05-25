from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import schemas, palindrome, database, models

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

@router.get("/", response_model=list[schemas.Detection])
def get_all_detections(db: Session = Depends(get_db)):
    result = db.execute(select(models.Detection))
    return result.scalars().all()

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