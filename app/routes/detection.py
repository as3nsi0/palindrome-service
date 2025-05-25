from fastapi import APIRouter

from app import schemas, palindrome

router = APIRouter(prefix="/detections", tags=["Detections"])

@router.post("/")
def check_palindrome(detection: schemas.Palindrome):
    is_palindrome = palindrome.is_palindrome(detection.text)
    return {"Message": f"The palindrome {detection.text} is: {is_palindrome}"}