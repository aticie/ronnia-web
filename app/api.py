from app.utils.database_wrapper import UserDatabase
from app.token_handling import get_token
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
user_db = UserDatabase()
user_db.initialize()


@app.get("/")
async def root(response: Response):
    index_page = RedirectResponse('/index.html')
    return index_page


@app.get("/osu_authorize")
async def get_link_details(response: Response):
    osu_token_api = "https://osu.ppy.sh/oauth/authorize?response_type=code"
    client_id = 'client_id=' + os.getenv('OSU_CLIENT_ID')
    redirect_uri = 'redirect_uri=' + os.getenv('OSU_REDIRECT_URI')
    scope = 'scope=identify'

    return RedirectResponse('&'.join([osu_token_api, client_id, redirect_uri, scope]))


@app.get("/twitch_authorize")
async def get_link_details(response: Response):
    osu_token_api = "https://id.twitch.tv/oauth2/authorize?response_type=code"
    client_id = 'client_id=' + os.getenv('TWITCH_CLIENT_ID')
    redirect_uri = 'redirect_uri=' + os.getenv('TWITCH_REDIRECT_URI')
    scope = 'scope=user:read:email'

    return RedirectResponse('&'.join([osu_token_api, client_id, redirect_uri, scope]))


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/identify")
async def osu_identify_user(code: str):
    token_endpoint = 'https://osu.ppy.sh/oauth/token'
    parameters = {"client_id": os.getenv('OSU_CLIENT_ID'),
                  "client_secret": os.getenv('OSU_CLIENT_SECRET'),
                  "code": code,
                  "grant_type": "authorization_code",
                  "redirect_uri": os.getenv('OSU_REDIRECT_URI')}

    access_token = await get_token(token_endpoint, parameters)
    headers = {'Authorization': f'Bearer {access_token}'}

    me_endpoint = 'https://osu.ppy.sh/api/v2/me/osu'
    return await fetch_user_from_token(headers, me_endpoint)


async def fetch_user_from_token(headers, me_endpoint):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(me_endpoint) as resp:
            me_result = await resp.json()
    if me_endpoint.endswith('osu'):
        user_id = me_result['id']
        user_details = user_db.get_user_from_osu_id(user_id)
        user_details['avatar_url'] = me_result['avatar_url']
    else:
        user_id = me_result['data'][0]['id']
        user_details = user_db.get_user_from_twitch_id(user_id)
        user_details['avatar_url'] = me_result['data'][0]['profile_image_url']

    encoded_jwt = create_access_token(user_details)
    to_me_page = RedirectResponse('/index.html')
    to_me_page.set_cookie('token', encoded_jwt)
    return to_me_page


@app.get('/twitch_identify')
async def twitch_identify_user(code: str, scope: str):
    token_endpoint = 'https://id.twitch.tv/oauth2/token'
    parameters = {"client_id": os.getenv('TWITCH_CLIENT_ID'),
                  "client_secret": os.getenv('TWITCH_CLIENT_SECRET'),
                  "code": code,
                  "grant_type": "authorization_code",
                  "redirect_uri": os.getenv('TWITCH_REDIRECT_URI')}

    access_token = await get_token(token_endpoint, parameters)
    headers = {'Authorization': f'Bearer {access_token}',
               'Client-Id': os.getenv('TWITCH_CLIENT_ID')}

    me_endpoint = 'https://api.twitch.tv/helix/users'

    return await fetch_user_from_token(headers, me_endpoint)


@app.get("/user_details")
async def get_user_details(jwt_token: str):
    user_data_dict = decode_jwt_token(jwt_token)
    print(user_data_dict)
    return user_data_dict


@app.get('/get_all_settings')
async def get_all_settings():
    return user_db.select_all_settings()


@app.get('/get_user_settings')
async def get_user_settings(user_id: str):
    return user_db.select_all_settings_by_user_id(user_id)


@app.post('/get_user_settings')
async def post_user_settings():
    return 


app.mount("/", StaticFiles(directory=os.path.join("frontend", "public")), name="public")
