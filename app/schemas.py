from pydantic import BaseModel
from datetime import datetime

class DetectionCreate(BaseModel):
    text: str
    language: str

class Detection(BaseModel):
    id: int
    text: str
    language: str
    is_palindrome: bool
    created_at: datetime

    class Config:
        from_attributes = True