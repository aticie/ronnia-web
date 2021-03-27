import os
import json

from dotenv import load_dotenv
import aiohttp
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from starlette.exceptions import HTTPException as StarletteHTTPException

from app.jwt import create_access_token, decode_jwt_token

load_dotenv()

app = FastAPI()


@app.get("/")
async def root(response: Response):
    index_page = RedirectResponse('/index.html')
    return index_page


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/identify")
async def identify_user(code: str):
    token_endpoint = 'https://osu.ppy.sh/oauth/token'
    parameters = {"client_id": os.getenv('CLIENT_ID'),
                  "client_secret": os.getenv('CLIENT_SECRET'),
                  "code": code,
                  "grant_type": "authorization_code",
                  "redirect_uri": os.getenv('REDIRECT_URI')}

    me_endpoint = 'https://osu.ppy.sh/api/v2/me/osu'

    async with aiohttp.ClientSession() as session:
        async with session.post(token_endpoint, data=parameters) as resp:
            token_result = json.loads(await resp.read())

    access_token = token_result['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(me_endpoint) as resp:
            me_result = await resp.json()

    user_id = me_result['id']

    encoded_jwt = create_access_token({'osu_user_id': user_id})

    to_me_page = RedirectResponse('/index.html')
    to_me_page.set_cookie('token', encoded_jwt)
    return to_me_page


@app.get("/user_details")
async def get_user_details(jwt_token: str):
    user_id = decode_jwt_token(jwt_token)

    return user_id


def add_user_to_db():
    return


app.mount("/", StaticFiles(directory=os.path.join("frontend", "public")), name="public")
