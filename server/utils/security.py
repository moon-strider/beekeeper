import os
import datetime
import logging

from logging.config import dictConfig
from logging_config import log_config
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt


dictConfig(log_config)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logging.debug(f"Password hasher prepared successfully...")


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt