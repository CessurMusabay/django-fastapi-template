from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from . import jwt

from django.contrib.auth import get_user_model
from typing import TypeAlias

USER_MODEL = get_user_model()
User: TypeAlias = USER_MODEL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
oauth2_scheme_refresh = OAuth2PasswordBearer(tokenUrl="/api/auth/token/refresh")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode_token(token)
    if payload is None or payload.sub is None:
        raise credentials_exception

    user = await USER_MODEL.objects.filter(id=payload.sub).afirst()
    if user is None:
        raise credentials_exception
    return user


async def is_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User '{user.username}' is not an admin. is_superuser={user.is_superuser}",
        )
    return user
