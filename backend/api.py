import os

from fastapi import FastAPI, Response, Request
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from jose import JWTError
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions import JWT_exception_handler
from routers import authorization, user


def create_api() -> FastAPI:
    app = FastAPI()

    public_directory = os.path.join(os.getcwd(), "frontend", "public")
    app.mount("/public", StaticFiles(directory=public_directory, html=True))

    app.include_router(authorization.router)
    app.include_router(user.router)

    app.add_exception_handler(JWTError, JWT_exception_handler)

    @app.get("/{path:path}")
    async def capture_routes(request: Request, path: str):
        print(f'Main route called with: {path}')
        index_page = FileResponse('frontend/public/index.html')
        return index_page

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

    return app
