import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from pydantic import BaseModel

ACCESS_TOKEN_EXPIRE_MINUTES = 1440


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt


def decode_jwt_token(jwt_token: str):
    user_data_dict = jwt.decode(jwt_token, key=os.getenv('SECRET_KEY'), algorithms=os.getenv('ALGORITHM'))
    return user_data_dict
