from unicodedata import normalize, category
from re import sub

SPECIAL_CHARACTERS = {"ñ": "A"}

def normalize_text(text: str) -> str:
    def __process_text(text: str, keep_mode: bool) -> str:
        if keep_mode:
            for special_character, replace_value in SPECIAL_CHARACTERS.items():
                text = text.replace(special_character, replace_value)
        else:
            for special_character, replace_value in SPECIAL_CHARACTERS.items():
                text = text.replace(replace_value, special_character)
        return text

    text = __process_text(text=text.lower(), keep_mode=True)
    text = normalize("NFD", text)
    text = "".join(c for c in text if category(c) != "Mn")
    text = __process_text(text=text, keep_mode=False)
    text = sub(r"[^a-zA-Z0-9ñÑ]", "", text).lower()
    return text

def is_palindrome(text: str) -> bool:
    cleaned = normalize_text(text)
    return cleaned == cleaned[::-1]