from unicodedata import normalize, category
from re import sub

def normalize_text(text: str) -> str:
    text = normalize('NFD', text)
    text = ''.join(c for c in text if category(c) != 'Mn')
    text = sub(r'[^a-zA-Z0-9]', '', text).lower()
    return text

def is_palindrome(text: str) -> bool:
    cleaned = normalize_text(text)
    return cleaned == cleaned[::-1]