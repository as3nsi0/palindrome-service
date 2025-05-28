from app.palindrome import normalize_text


def test_normalize_text_with_accents_and_special_characters():
    assert normalize_text("¿Hola, como estás?") == "holacomoestas"


def test_normalize_text_with_special_character():
    assert normalize_text("Español") == "español"