from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from .schemas import TokenPayload

import os
from datetime import timedelta
from django.contrib.auth import get_user_model
from config import settings


JWT_SECRET_KEY = settings.secret_key.get_secret_value()
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = settings.access_token_expire_days
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

user_model = get_user_model()


async def authenticate_user(username: str, password: str):
    user = await user_model.objects.filter(username=username).afirst()
    if user and user.check_password(password):
        return user
    return None


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "token_type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt, expire


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt, expire


def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return TokenPayload(**payload)
    except jwt.PyJWTError:
        return None


def decode_refresh_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("token_type") != "refresh":
            return None
        return TokenPayload(**payload)
    except jwt.PyJWTError:
        return None


async def get_current_user_from_refrefh_token(token: str):
    payload = decode_refresh_token(token)
    if payload is None or payload.sub is None:
        return None
    user = await user_model.objects.filter(id=payload.sub).afirst()
    return user
