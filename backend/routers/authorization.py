import os
from typing import Optional

import aiohttp
from fastapi import APIRouter, Response, Cookie
from starlette.responses import RedirectResponse, FileResponse

from backend.utils.database_wrapper import UserDatabase
from backend.utils.jwt import obtain_jwt
from backend.utils.signup import RegisterOsu, RegisterTwitch
from backend.utils.token_handling import get_token
from utils.tcp import signup_user_over_tcp_async

router = APIRouter()

user_db = UserDatabase()
user_db.initialize()


@router.get("/osu_authorize")
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


@router.get("/twitch_authorize")
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


@router.get("/identify")
async def osu_identify_user(code: Optional[str] = None, error: Optional[str] = None,
                            user_details: Optional[str] = Cookie(None)):
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
    return await fetch_user_from_token(headers, me_endpoint, user_details)


@router.get('/twitch_identify')
async def twitch_identify_user(code: Optional[str] = None, error: Optional[str] = None,
                               user_details: Optional[str] = Cookie(None)):
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
    return await fetch_user_from_token(headers, me_endpoint, user_details)


async def fetch_user_from_token(headers, me_endpoint, user_details_jwt: Optional[str] = None):
    # Get user details with given token
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(me_endpoint) as resp:
            me_result = await resp.json()

    # If a user is not found -> keep user details in cookie, send them to the sign-up page
    if me_endpoint.endswith('osu'):
        registerer = RegisterOsu(me_result, user_db)
    else:
        registerer = RegisterTwitch(me_result, user_db)

    try:
        user_details = registerer.get_user()
    except (IndexError, TypeError):
        signup_details = registerer.signup_user(user_details_jwt)
        if isinstance(signup_details, RedirectResponse):
            return signup_details
        else:
            response = await signup_user_over_tcp_async(signup_details)
            to_me_page = RedirectResponse('/settings')
            to_me_page.set_cookie('token', obtain_jwt(response['user']))
            return to_me_page

    encoded_jwt = obtain_jwt(user_details)
    to_settings_page = RedirectResponse('/settings')
    to_settings_page.set_cookie('token', encoded_jwt)

    return to_settings_page
