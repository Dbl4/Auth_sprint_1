import hashlib
import os
import uuid
from datetime import timedelta

from email_validator import validate_email, EmailNotValidError
from flask import abort
from flask_jwt_extended import create_access_token, decode_token


def is_valid_email(email: str) -> str:
    try:
        return validate_email(email).email
    except EmailNotValidError as err:
        abort(422, description="Email is not valid.")


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


def create_tokens(identity: str, additional_claims: dict) -> tuple[str, str]:
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=timedelta(minutes=5)
    )
    refresh_token = uuid.uuid4()
    return access_token, refresh_token


def put_rftoken_db(user_id: uuid, access_token: str, refresh_token: str) -> None:
    decoded_token = decode_token(access_token)
    jti = decoded_token["jti"]
    rftoken_to_redis = f"{user_id}:{jti} {refresh_token}"
    ## save redis rftoken_to_redis


def is_correct_token():
    # в базе будут храниться токены, будем проверять,
    # есть ли приходящий рефреш токен в базе.
    pass
