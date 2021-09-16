from fastapi import HTTPException, Request
from jose import JWTError
from starlette.responses import RedirectResponse


class SignupException(JWTError):
    pass


def JWT_exception_handler(request: Request, exc: HTTPException):
    to_main_page = RedirectResponse('/')
    to_main_page.delete_cookie('user_details')
    to_main_page.delete_cookie('signup')
    return to_main_page