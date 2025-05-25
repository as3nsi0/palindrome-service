from pydantic import BaseModel

class Palindrome(BaseModel):
    text: str
    language: str