import logging
import os
from typing import Optional

import aiohttp
from fastapi import APIRouter, Response, Cookie, HTTPException
from starlette.responses import RedirectResponse, FileResponse

from backend.utils.jwt import obtain_jwt
from backend.utils.signup import RegisterFactory
from backend.utils.token_handling import get_token
from utils.globals import USER_DB
from utils.service_bus import signup_user_over_mq

router = APIRouter()
logger = logging.getLogger("ronnia-web")
logger.debug("Authorization router loaded")


@router.get("/osu_authorize")
async def osu_authorize(response: Response):
    """
    osu! authorization endpoint

    Should redirect to https://osu.ppy.sh/oauth/authorize
    """
    logger.debug("osu! authorization requested, redirecting to osu!")
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
    logger.debug("twitch authorization requested, redirecting to twitch")
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

    logger.debug("osu! callback received, getting oauth token...")
    token_endpoint = 'https://osu.ppy.sh/oauth/token'
    parameters = {"client_id": os.getenv('OSU_CLIENT_ID'),
                  "client_secret": os.getenv('OSU_CLIENT_SECRET'),
                  "code": code,
                  "grant_type": "authorization_code",
                  "redirect_uri": os.getenv('OSU_REDIRECT_URI')}

    token_details = await get_token(token_endpoint, parameters)
    logger.debug(f"Got token details: {token_details}")
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


async def fetch_user_from_token(headers, me_endpoint, user_details_jwt: Optional[str] = None,
                                signup_type: Optional[str] = Cookie(None)):
    # Get user details with given token

    logger.debug(f"fetch_user_from_token called with: headers: {headers}, me_endpoint: {me_endpoint},"
                 f" user_details_jwt: {user_details_jwt}")
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(me_endpoint) as resp:
            me_result = await resp.json()

    logger.debug(f"Got me details: {me_result}")
    registerer = RegisterFactory(USER_DB).get_register_class(me_result)

    logger.debug(f"Initialized registerer as: {type(registerer)}")
    try:
        user_details = await registerer.get_user()
        logger.debug(f"Found user in the database: {user_details}")

        encoded_jwt = obtain_jwt(user_details)
        to_settings_page = RedirectResponse('/settings')
        to_settings_page.set_cookie('token', encoded_jwt)

        logger.debug(f"Redirecting to settings page...")

        return to_settings_page

    except (IndexError, TypeError):
        # If the user is not in the database, start signup process
        logger.debug(f"User not found in the database, starting signup process...")
        signup_details = registerer.signup_user(user_details_jwt)
        if isinstance(signup_details, RedirectResponse):
            return signup_details

        else:
            # We can sign-up the user by sending a message to message queue.
            logger.debug(f"Sending sign-up details to the bot manager...")
            response = await signup_user_over_mq(signup_details)

            if signup_type == 'osu':
                response['username'] = response['osu_username']
            else:
                response['username'] = response['twitch_username']

            to_me_page = RedirectResponse('/settings')
            to_me_page.set_cookie('token', obtain_jwt(response))
            return to_me_page
