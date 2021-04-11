import sqlite3
import os


class BaseDatabase:
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.conn: sqlite3.Connection = None
        self.c: sqlite3.Cursor = None

    def initialize(self):
        self.conn = sqlite3.connect(self.db_path,
                                    check_same_thread=False,
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def dispose(self):
        self.conn.close()
        os.remove(self.db_path)
        del self


class UserDatabase(BaseDatabase):
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.getenv('DB_DIR'), 'users.db')
        super().__init__(db_path)

    def initialize(self):
        super().initialize()

    def get_user_from_twitch_id(self, twitch_id: str):
        self.c.execute('SELECT * FROM users WHERE twitch_id=?', (twitch_id,))
        user_details = self.c.fetchone()
        user_json = dict(user_details)
        del user_json['updated_at']
        return user_json

    def get_user_from_osu_id(self, osu_id: str):
        self.c.execute('SELECT * FROM users WHERE osu_id=?', (osu_id,))
        user_details = self.c.fetchone()
        user_json = dict(user_details)
        del user_json['updated_at']
        return user_json

    def select_all_settings(self):
        self.c.execute('SELECT * FROM settings')
        all_settings = [dict(setting) for setting in self.c.fetchall()]
        return all_settings

    def select_all_settings_by_user_id(self, user_id: str):
        self.c.execute('SELECT * FROM user_settings WHERE user_id=?', (user_id,))
        user_settings = {setting['key']: setting['value'] for setting in self.c.fetchall()}
        return user_settings
