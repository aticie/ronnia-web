import os
import sqlite3
from typing import Optional

import aiosqlite

from models.user import DBUser


class BaseDatabase:
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.conn: Optional[aiosqlite.Connection] = None
        self.c: Optional[aiosqlite.Cursor] = None

    async def initialize(self):
        self.conn = await aiosqlite.connect(self.db_path,
                                            check_same_thread=False,
                                            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.conn.row_factory = aiosqlite.Row
        self.c = await self.conn.cursor()

    async def dispose(self):
        await self.conn.close()
        os.remove(self.db_path)
        del self


class UserDatabase(BaseDatabase):
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.getenv('DB_DIR'), 'users.db')
        super().__init__(db_path)

    async def get_user_from_twitch_id(self, twitch_id: str) -> DBUser:
        await self.c.execute('SELECT * FROM users WHERE twitch_id=?', (twitch_id,))
        user_details = await self.c.fetchone()
        return DBUser.from_sqlite_row(user_details)

    async def get_user_from_osu_id(self, osu_id: str) -> DBUser:
        await self.c.execute('SELECT * FROM users WHERE osu_id=?', (osu_id,))
        user_details = await self.c.fetchone()
        return DBUser.from_sqlite_row(user_details)

    async def select_all_settings(self):
        await self.c.execute('SELECT * FROM settings')
        all_settings = await self.c.fetchall()
        toggle_settings = [{**dict(setting), **{'type': 'toggle', 'value': setting['default_value']}}
                           for setting in all_settings]

        await self.c.execute('SELECT * FROM range_settings')
        all_range_settings = await self.c.fetchall()
        range_settings = [{**dict(setting), **{'type': 'range', 'range_start': setting['default_low'],
                                               'range_end': setting['default_high']}} for setting in all_range_settings]

        return toggle_settings + range_settings

    async def select_all_settings_by_user_id(self, user_id: str):
        all_settings = await self.select_all_settings()
        await self.c.execute('SELECT * FROM user_settings WHERE user_id=?', (user_id,))
        set_user_settings = await self.c.fetchall()
        user_settings = [{**dict(setting), **{'type': 'toggle'}} for setting in
                         set_user_settings]

        for setting in user_settings:
            user_setting_key = setting['key']
            for default_setting in all_settings:
                if default_setting['key'] == user_setting_key:
                    default_setting['value'] = setting['value']
                    break

        await self.c.execute('SELECT * FROM user_range_settings WHERE user_id=?', (user_id,))
        set_user_range_settings = await self.c.fetchall()
        user_range_settings = [{**dict(setting), **{'type': 'range'}} for setting in
                               set_user_range_settings]

        for setting in user_range_settings:
            user_setting_key = setting['key']
            for default_setting in all_settings:
                if default_setting['key'] == user_setting_key:
                    default_setting['range_start'] = setting['range_start']
                    default_setting['range_end'] = setting['range_end']
                    break

        return all_settings

    async def set_setting(self, user_id, setting_key, new_value):
        """
        Set a new value for a setting of user
        :param user_id: User id in database
        :param setting_key: Setting key
        :param new_value: New value of the desired setting
        :return:
        """
        sql_string_get_setting = f"SELECT value FROM user_settings " \
                                 f"INNER JOIN settings ON user_settings.key=settings.key " \
                                 f"WHERE settings.key=? AND user_id=?"

        sql_string_insert_setting = f"INSERT INTO user_settings (key, value, user_id) " \
                                    f"VALUES (?1, ?2, ?3);"

        sql_string_update_setting = f"UPDATE user_settings SET value=?2 WHERE key=?1 AND user_id=?3"

        result = await self.c.execute(sql_string_get_setting, (setting_key, user_id))
        value = await result.fetchone()
        if value is None:
            await self.c.execute(sql_string_insert_setting, (setting_key, new_value, user_id))
        else:
            await self.c.execute(sql_string_update_setting, (setting_key, new_value, user_id))
        await self.conn.commit()
        return new_value

    async def set_range_setting(self, user_id, setting_key: str, range_low: float, range_high: float):
        """
        Sets a range setting with given key
        :param user_id: User id in database
        :param setting_key: Setting key
        :param range_low: Lower value of the range
        :param range_high: Higher value of the range
        :return: Tuple: New range values
        """
        if range_high != -1 and range_low != -1:
            assert range_high > range_low, 'Max value cannot be lower than min value.'

        sql_string_get_range_setting = f"SELECT range_start, range_end FROM user_range_settings " \
                                       f"INNER JOIN range_settings ON user_range_settings.key=range_settings.key " \
                                       f"WHERE user_range_settings.key=? AND user_id=?"

        sql_string_insert_range_setting = f"INSERT INTO user_range_settings (key, range_start, range_end, user_id) " \
                                          f"VALUES (?1, ?2, ?3, ?4);"

        sql_string_update_range_setting = f"UPDATE user_range_settings SET range_start=?2, range_end=?3 " \
                                          f"WHERE key=?1 AND user_id=?4"

        result = await self.c.execute(sql_string_get_range_setting, (setting_key, user_id))
        value = await result.fetchone()
        if value is None:
            await self.c.execute(sql_string_insert_range_setting, (setting_key, range_low, range_high, user_id))
        else:
            await self.c.execute(sql_string_update_range_setting, (setting_key, range_low, range_high, user_id))
        await self.conn.commit()
        return range_low, range_high
