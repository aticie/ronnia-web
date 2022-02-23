from fastapi import HTTPException, Request
from jose import JWTError


class SignupException(JWTError):
    pass


def JWT_exception_handler(request: Request, exc: HTTPException):
    raise HTTPException(500, str(exc))
