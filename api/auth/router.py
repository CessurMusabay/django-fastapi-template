from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Token
from . import jwt


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await jwt.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, expire = jwt.create_access_token(data={"sub": str(user.id)})
    refresh_token, _expire = jwt.create_refresh_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expires": expire,
        "refresh_token_expires": _expire,
    }


@router.post("/token/refresh", response_model=Token)
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    user = await jwt.get_current_user_from_refrefh_token(refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, expire = jwt.create_access_token(data={"sub": str(user.id)})
    refresh_token, _expire = jwt.create_refresh_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expires": expire,
        "refresh_token_expires": _expire,
    }
