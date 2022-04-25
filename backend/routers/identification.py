import logging
import os
from typing import Optional

import aiohttp
from fastapi import Cookie, APIRouter
from starlette.responses import RedirectResponse

from utils.globals import USER_DB
from utils.signup import RegisterFactory

router = APIRouter()
logger = logging.getLogger('ronnia-web')


class Identifier:
    def __init__(self):
        self.token_endpoint = None
        self.me_endpoint = None

        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None
        self.grant_type = None
        self.code = None

        self.access_token = None
        self.token_type = None
        self.headers = None

        self.me_response = None

    async def get_token(self):
        logger.debug("Getting oauth token...")
        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_endpoint, data={
                'grant_type': self.grant_type,
                'code': self.code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    logger.error(f"error getting token: {resp.status}")
                    raise Exception(f"error getting access token from {self.token_endpoint}: {resp.status}")

    async def identify(self, code: Optional[str] = None, error: Optional[str] = None,
                       user_details: Optional[str] = Cookie(None)):
        logger.debug(f"{self.__class__.__name__} callback received, getting oauth token...")

        if error is not None or code is None:
            return RedirectResponse('/')

        self.code = code
        token_details = await self.get_token()
        logger.debug(f"Got token details: {token_details}")

        self.access_token: str = token_details['access_token']
        self.token_type: str = token_details['token_type'].capitalize()

        await self.set_headers()

        await self.fetch_user_with_token(user_details)

    async def set_headers(self):
        raise NotImplementedError

    async def fetch_user_with_token(self, user_details: Optional[str] = None):
        logger.debug(f"Fetching user details with the given token...")
        async with aiohttp.ClientSession() as session:
            async with session.get(self.me_endpoint, headers=self.headers) as resp:
                self.me_response = await resp.json()

        registerer = RegisterFactory(USER_DB).get_register_class(self.me_response)

        try:
            user_db_details = await registerer.get_user()
        except (IndexError, TypeError) as e:
            logger.debug(f"User not found in database, registering...")
            signup_details = await registerer.signup_user(user_details)



class OsuIdentifier(Identifier):
    def __init__(self):
        super().__init__()
        self.token_endpoint = 'https://osu.ppy.sh/oauth/token'
        self.me_endpoint = 'https://osu.ppy.sh/api/v2/me/osu'

        self.client_id = os.getenv('OSU_CLIENT_ID')
        self.client_secret = os.getenv('OSU_CLIENT_SECRET')
        self.redirect_uri = os.getenv('OSU_REDIRECT_URI')
        self.grant_type = 'authorization_code'

    @router.get('/osu/callback')
    async def identify(self, code: Optional[str] = None, error: Optional[str] = None,
                       user_details: Optional[str] = Cookie(None)):
        await super(OsuIdentifier, self).identify(code, error, user_details)

    async def set_headers(self):
        self.headers = {'Authorization': f'{self.token_type} {self.access_token}'}


class TwitchIdentifier(Identifier):
    def __init__(self):
        super().__init__()
        self.token_endpoint = 'https://id.twitch.tv/oauth2/token'
        self.me_endpoint = 'https://api.twitch.tv/helix/users'

        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.redirect_uri = os.getenv('TWITCH_REDIRECT_URI')
        self.grant_type = 'authorization_code'

    @router.get('/twitch/callback')
    async def identify(self, code: Optional[str] = None, error: Optional[str] = None,
                       user_details: Optional[str] = Cookie(None)):
        await super(TwitchIdentifier, self).identify(code, error, user_details)

    async def set_headers(self):
        self.headers = {'Authorization': f'{self.token_type} {self.access_token}',
                        'Client-Id': self.client_id}
