import os
from typing import Optional

import aiohttp
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse, PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.jwt import create_access_token, decode_jwt_token
from backend.models.setting import UserSetting
from backend.token_handling import get_token
from backend.utils.database_wrapper import UserDatabase
from backend.utils.signup import RegisterOsu, RegisterTwitch

app = FastAPI()
user_db = UserDatabase()
user_db.initialize()

@app.get("/")
async def root(response: Response):
    index_page = FileResponse('frontend/public/index.html')
    return index_page


@app.get("/osu_authorize")
async def osu_authorize(response: Response):
    """
    osu! authorization endpoint

    Should redirect to https://osu.ppy.sh/oauth/authorize
    """
    osu_token_api = "https://osu.ppy.sh/oauth/authorize?response_type=code"
    client_id = 'client_id=' + os.getenv('OSU_CLIENT_ID')
    redirect_uri = 'redirect_uri=' + os.getenv('OSU_REDIRECT_URI')
    scope = 'scope=identify'

    return RedirectResponse('&'.join([osu_token_api, client_id, redirect_uri, scope]))


@app.get("/twitch_authorize")
async def twitch_authorize(response: Response):
    """
    Twitch authorization endpoint

    Should redirect to https://id.twitch.tv/oauth2/authorize
    """
    osu_token_api = "https://id.twitch.tv/oauth2/authorize?response_type=code"
    client_id = 'client_id=' + os.getenv('TWITCH_CLIENT_ID')
    redirect_uri = 'redirect_uri=' + os.getenv('TWITCH_REDIRECT_URI')
    scope = 'scope=user:read:email'

    return RedirectResponse('&'.join([osu_token_api, client_id, redirect_uri, scope]))


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/identify")
async def osu_identify_user(code: Optional[str] = None, error: Optional[str] = None):
    """
    Identify user over osu!:
    - **code**: Code supplied from osu! api
    - **error**: If an error happened or not while identifying
    """
    if error is not None or code is None:
        return FileResponse('frontend/public/index.html')

    token_endpoint = 'https://osu.ppy.sh/oauth/token'
    parameters = {"client_id": os.getenv('OSU_CLIENT_ID'),
                  "client_secret": os.getenv('OSU_CLIENT_SECRET'),
                  "code": code,
                  "grant_type": "authorization_code",
                  "redirect_uri": os.getenv('OSU_REDIRECT_URI')}

    token_details = await get_token(token_endpoint, parameters)
    access_token: str = token_details['access_token']
    token_type: str = token_details['token_type']
    headers = {'Authorization': f'{token_type.capitalize()} {access_token}'}

    me_endpoint = 'https://osu.ppy.sh/api/v2/me/osu'
    return await fetch_user_from_token(headers, me_endpoint)


async def fetch_user_from_token(headers, me_endpoint):

    # Get user details with given token
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(me_endpoint) as resp:
            me_result = await resp.json()

    to_me_page = FileResponse('frontend/public/index.html')

    # If a user is not found -> keep user details in cookie, send them to the sign-up page
    if me_endpoint.endswith('osu'):
        registerer = RegisterOsu(me_result, user_db)
    else:
        registerer = RegisterTwitch(me_result, user_db)

    try:
        user_details = registerer.get_user()
    except (IndexError, TypeError):
        registerer.set_cookies(to_me_page)
        return to_me_page

    encoded_jwt = create_access_token(user_details)
    to_me_page.set_cookie('token', encoded_jwt)

    return to_me_page


@app.get('/twitch_identify')
async def twitch_identify_user(code: Optional[str] = None, error: Optional[str] = None):
    """
        Identify user over twitch:
        - **code**: Code supplied from twitch api
        - **error**: If an error happened or not while identifying
    """

    # If there was an error, return to index without logging in.
    if error is not None or code is None:
        return FileResponse('frontend/public/index.html')

    # Get access token for the user
    token_endpoint = 'https://id.twitch.tv/oauth2/token'
    parameters = {"client_id": os.getenv('TWITCH_CLIENT_ID'),
                  "client_secret": os.getenv('TWITCH_CLIENT_SECRET'),
                  "code": code,
                  "grant_type": "authorization_code",
                  "redirect_uri": os.getenv('TWITCH_REDIRECT_URI')}

    token_details = await get_token(token_endpoint, parameters)
    token_type = token_details["token_type"].capitalize()
    access_token = token_details["access_token"]
    headers = {'Authorization': f'{token_type} {access_token}',
               'Client-Id': os.getenv('TWITCH_CLIENT_ID')}

    me_endpoint = 'https://api.twitch.tv/helix/users'

    # Return to settings page after fetching user details
    return await fetch_user_from_token(headers, me_endpoint)


@app.get("/user_details", summary='Gets registered user details from database')
async def get_user_details(jwt_token: str):
    """
        Get registered user details from database:
        - **jwt_token**: JWT token of the current user
    """
    user_data_dict = decode_jwt_token(jwt_token)
    user_id = user_data_dict['user_id']
    user_settings = user_db.select_all_settings_by_user_id(user_id)
    user_data_dict['settings'] = user_settings
    return user_data_dict


@app.post('/save_user_settings', summary="Save user settings")
async def save_user_settings(payload: UserSetting):
    """
    Saves user settings:

    - **settings**: List of settings to be updated
      - **echo**: Twitch chat feedback setting
      - **enable**: Bot enable/disable setting
      - **sub-only**: Subscriber only mode setting
      - **cp-only**: Channel points only mode setting
      - **sr**: Star rating RangeSetting
    - **jwt_token**: JWT token of the current user
    """
    settings = payload.settings
    jwt_token = payload.jwt_token
    user_data = decode_jwt_token(jwt_token=jwt_token)
    user_id = user_data['user_id']
    for setting in settings:
        if setting.type == 'toggle':
            user_db.set_setting(user_id=user_id, setting_key=setting.key, new_value=setting.value)
        elif setting.type == 'range':
            user_db.set_range_setting(user_id=user_id, setting_key=setting.key, range_low=setting.range_start,
                                      range_high=setting.range_end)

    return

app.mount("/", StaticFiles(directory=os.path.join("frontend", "public")), name="public")

