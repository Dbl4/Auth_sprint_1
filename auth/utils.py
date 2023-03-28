import hashlib
import os

from flask_jwt_extended import create_access_token, create_refresh_token


def hash_password(password: str) -> str:
    salt = os.urandom(32)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}&{pw_hash.hex()}"


def is_correct_password(correct_password: str, entered_password: str) -> bool:
    salt, correct_pw_hash = correct_password.split("&")
    entered_pw_hash = hashlib.pbkdf2_hmac(
        "sha256", entered_password.encode("utf-8"), bytes.fromhex(salt), 100000
    )
    if correct_pw_hash == str(entered_pw_hash.hex()):
        return True
    return False


def create_tokens(identity: str) -> tuple[str, str]:
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token


def is_correct_token():
    # в базе будут храниться токены, будем проверять,
    # есть ли приходящий рефреш токен в базе.
    pass
