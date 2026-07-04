import os
from datetime import datetime, timedelta
from typing import Any

import bcrypt
import jwt
from jwt import PyJWTError

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set.")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 60 * 24


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_passwoprd: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"), hashed_passwoprd.encode("utf-8")
    )


def create_access_token(
    subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE
) -> str:
    expire = datetime.now() + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except PyJWTError as ex:
        raise ValueError("Invalid token") from ex
