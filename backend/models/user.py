import datetime
from dataclasses import dataclass
from typing import Tuple


@dataclass
class DBUser(object):
    user_id: str
    osu_username: str
    twitch_username: str
    enabled: str
    twitch_id: str
    osu_id: str
    updated_at: datetime.datetime

    @classmethod
    def from_sqlite_row(cls, row: Tuple):
        return cls(*row)
