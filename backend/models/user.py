import datetime
from typing import Tuple


class DBUser(object):

    def __init__(self, user_id: int, osu_username: str, twitch_username: str, enabled: int, twitch_id: str, osu_id: str,
                 updated_at: datetime.datetime):
        self.user_id = user_id
        self.osu_username = osu_username
        self.twitch_username = twitch_username
        self.enabled = enabled
        self.twitch_id = twitch_id
        self.osu_id = osu_id
        self.updated_at = updated_at

    @classmethod
    def from_sqlite_row(cls, row: Tuple):
        return cls(*row)
