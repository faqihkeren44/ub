import secrets
import string
import random

def generate_password(length: int = 8) -> str:
    """
    Generate password dengan ketentuan:
    - Minimal 8 karakter
    - Mengandung minimal 1 huruf kecil
    - Mengandung minimal 1 huruf besar
    - Mengandung minimal 1 angka
    """

    if length < 8:
        raise ValueError("Panjang password minimal password 8 karakter")

    lowercase = secrets.choice(string.ascii_lowercase)
    uppercase = secrets.choice(string.ascii_uppercase)
    digit = secrets.choice(string.digits)

    all_chars = string.ascii_letters + string.digits
    remaining = [
        secrets.choice(all_chars)
        for _ in range(length - 3)
    ]

    password_chars = [lowercase, uppercase, digit] + remaining

    random.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)