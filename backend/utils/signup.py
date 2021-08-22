import json
from typing import Optional

from fastapi.responses import FileResponse

from backend.utils.database_wrapper import UserDatabase


class RegisterBase:
    def __init__(self, user_db: UserDatabase):
        self.details: Optional[dict] = None
        self.user_db = user_db

    def get_user(self):
        raise NotImplementedError

    def set_cookies(self, page_that_needs_cookies: FileResponse):
        # Sets cookie key-value to user details
        page_that_needs_cookies.set_cookie('user_details', json.dumps(self.details))
        return


class RegisterOsu(RegisterBase):

    def __init__(self, osu_details: dict, user_db: UserDatabase):
        super().__init__(user_db)
        self.details = osu_details
        self.avatar_url = self.details['avatar_url']
        self.id = osu_details['id']

    def get_user(self):
        return {**self.user_db.get_user_from_osu_id(self.id), **{'avatar_url': self.avatar_url}}

    def set_cookies(self, page_that_needs_cookies: FileResponse):
        super(RegisterOsu, self).set_cookies(page_that_needs_cookies)
        page_that_needs_cookies.set_cookie('signup', 'osu')
        return


class RegisterTwitch(RegisterBase):

    def __init__(self, twitch_details: dict, user_db: UserDatabase):
        super().__init__(user_db)
        self.details = twitch_details['data'][0]
        self.avatar_url = self.details['profile_image_url']
        self.id = self.details['id']

    def get_user(self):
        return {**self.user_db.get_user_from_osu_id(self.id), **{'avatar_url': self.avatar_url}}

    def set_cookies(self, page_that_needs_cookies: FileResponse):
        super(RegisterTwitch, self).set_cookies(page_that_needs_cookies)
        page_that_needs_cookies.set_cookie('signup', 'twitch')
        return
