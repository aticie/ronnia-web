import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from jose import JWTError
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions import JWT_exception_handler
from routers import authorization, user
from utils.globals import USER_DB

logger = logging.getLogger('ronnia-web')
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())
loggers_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(process)d | %(name)s | %(funcName)s | %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S')

ch = logging.StreamHandler()
ch.setFormatter(loggers_formatter)
logger.addHandler(ch)

logger.propagate = False


def create_api() -> FastAPI:
    app = FastAPI()

    public_directory = os.path.join(os.getcwd(), "frontend", "public")
    app.mount("/public", StaticFiles(directory=public_directory, html=True))

    app.include_router(authorization.router)
    app.include_router(user.router)

    app.add_exception_handler(JWTError, JWT_exception_handler)

    @app.on_event("startup")
    async def startup_event():
        logger.debug("Initializing database...")

        # Create database
        await USER_DB.initialize()

        logger.debug("API started.")

    @app.get("/{path:path}")
    async def capture_routes(request: Request, path: str):
        logger.debug(f'Main route called with: {path}')
        index_page = FileResponse('frontend/public/index.html')
        return index_page

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

    return app
