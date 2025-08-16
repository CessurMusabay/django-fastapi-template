from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires: datetime
    refresh_token_expires: datetime


class TokenPayload(BaseModel):
    sub: Optional[int] = None
