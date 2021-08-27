import os
from queue import Queue
from threading import Thread
from typing import Optional

from fastapi.responses import Response
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from backend.utils.database_wrapper import UserDatabase
from models.user import DBUser
from utils.jwt import obtain_jwt, decode_jwt
from utils.tcp import signup_user_over_tcp


class RegisterBase:
    def __init__(self, user_db: UserDatabase):
        self.avatar_url = None
        self.details: Optional[dict] = None
        self.user_db = user_db

    def get_user(self):
        raise NotImplementedError

    def set_cookies(self, page_that_needs_cookies: Response):
        # Sets cookie key-value to user details
        page_that_needs_cookies.set_cookie('user_details', obtain_jwt(self.details))
        return page_that_needs_cookies

    def signup_user(self, extra_details_jwt: Optional[str] = None):
        # Redirect user to sign-up page if information is not complete
        if extra_details_jwt is None:
            to_signup_page = RedirectResponse('/signup')
            to_signup_page_with_cookies = self.set_cookies(to_signup_page)
            return to_signup_page_with_cookies
        else:
            extra_details = decode_jwt(extra_details_jwt)
            # If user somehow signed up with twitch twice or osu twice, we need to start again.
            if self._get_self_name() == extra_details.get('signup_data'):
                to_main_page = RedirectResponse('/')
                to_main_page.delete_cookie('user_details')
                return to_main_page
            else:
                # If user signed up with osu, get osu details from cookie jwt token.
                if extra_details.get('signup_data') == 'osu':
                    osu_details = extra_details
                    twitch_details = self.details
                # Else if user signed up with twitch, get twitch details from cookie jwt token.
                else:
                    osu_details = self.details
                    twitch_details = extra_details

                signup_data = {
                    'command': 'signup',
                    'osu_username': osu_details.get('username'),
                    'osu_id': osu_details.get('id'),
                    'twitch_username': twitch_details.get('login'),
                    'twitch_id': twitch_details.get('id')
                }

                # Send sign-up data over tcp to Ronnia-Bot!
                message_queue = Queue()
                p = Thread(target=signup_user_over_tcp,
                           args=(signup_data, message_queue, os.getenv('TCP_CONN_SECRET_KEY')))
                p.start()

                # Wait for response
                p.join()
                result: dict = message_queue.get()
                if result['status'] == 'OK':
                    dbuser : DBUser = result['user']
                    user_details = {
                        "username": osu_details.get('username'),
                        "avatar_url": self.avatar_url,
                        "user_id": dbuser.user_id,
                    }
                else:
                    raise HTTPException(status_code=500, detail="Something went wrong while signing you up!"
                                                                " I'm sorry, please try again!")

                to_me_page = RedirectResponse('/settings')
                to_me_page.set_cookie('token', obtain_jwt(user_details))
                return to_me_page

    def _get_self_name(self):
        return 'base'


class RegisterOsu(RegisterBase):

    def __init__(self, osu_details: dict, user_db: UserDatabase):
        super().__init__(user_db)
        self.details = osu_details
        self.avatar_url = self.details['avatar_url']
        self.id = osu_details['id']

    def get_user(self):
        user = self.user_db.get_user_from_osu_id(self.id)
        return {'username': user.osu_username,
                'user_id': user.user_id,
                'avatar_url': self.avatar_url}

    def set_cookies(self, page_that_needs_cookies: Response):
        self.details = {**self.details, **{'signup_data': 'osu'}}
        page_with_some_cookies = super(RegisterOsu, self).set_cookies(page_that_needs_cookies)
        page_with_some_cookies.set_cookie('signup', 'osu')
        return page_with_some_cookies

    def _get_self_name(self):
        return 'osu'


class RegisterTwitch(RegisterBase):

    def __init__(self, twitch_details: dict, user_db: UserDatabase):
        super().__init__(user_db)
        self.details = twitch_details['data'][0]
        self.avatar_url = self.details['profile_image_url']
        self.id = self.details['id']

    def get_user(self):
        user = self.user_db.get_user_from_twitch_id(self.id)
        return {'username': user.twitch_username,
                'user_id': user.user_id,
                'avatar_url': self.avatar_url}

    def set_cookies(self, page_that_needs_cookies: Response):
        self.details = {**self.details, **{'signup_data': 'twitch'}}
        page_with_some_cookies = super(RegisterTwitch, self).set_cookies(page_that_needs_cookies)
        page_with_some_cookies.set_cookie('signup', 'twitch')
        return page_with_some_cookies

    def _get_self_name(self):
        return 'twitch'
