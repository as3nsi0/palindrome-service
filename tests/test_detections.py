from app.palindrome import is_palindrome

def test_english_palindrome():
    assert is_palindrome("Able was I ere I saw Elba")

def test_spanish_palindrome():
    assert is_palindrome("Dábale arroz a la zorra el abad")

def test_not_palindrome():
    assert not is_palindrome("Este ejemplo no es un palíndromo")

def test_palindrome_with_special_character():
    assert is_palindrome("Ñoño rañón, noñar oñoñ.")