from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DetectionCreate(BaseModel):
    text: str
    language: str

class Detection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    language: str
    is_palindrome: bool
    created_at: datetime