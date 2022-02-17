import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 1440
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


def obtain_jwt(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(jwt_token: str):
    user_data_dict = jwt.decode(jwt_token, key=SECRET_KEY, algorithms=ALGORITHM)
    return user_data_dict
