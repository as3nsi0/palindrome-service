from app.utils import logger_config

from datetime import datetime
from http.client import HTTPException
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas, database, crud

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
    return crud.create_detection(detection=detection,
                                 db=db)

@router.get("/", response_model=List[schemas.Detection])
def list_detections(language: Optional[str] = Query(default=None,
                                                    description="Filter by language",
                                                    example="Spanish",
                                                    regex="^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]+$"),
                    start_date: Optional[datetime] = Query(default=None,
                                                           description="Filter by language (ISO 8601)",
                                                           example="2025-05-23T16:11:54"),
                    end_date: Optional[datetime] = Query(default=None,
                                                         description="Filter to date (ISO 8601)",
                                                         example="2025-05-26T16:11:54"),
                    db: Session = Depends(get_db)):

    return crud.list_detections(language=language,
                                start_date=start_date,
                                end_date=end_date,
                                db=db)

@router.get("/{detection_id}", response_model=schemas.Detection)
def find_specific_detection(detection_id: int,
                            db: Session = Depends(get_db)):
    detection = crud.find_specific_detection(detection_id=detection_id,
                                 db=db)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection

@router.delete("/{detection_id}", response_model=schemas.Detection)
def delete_detection(detection_id: int, db: Session = Depends(get_db)):
    detection = crud.delete_detection(detection_id=detection_id,
                          db=db)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")

    return detection
