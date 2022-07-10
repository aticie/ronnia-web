import logging

from fastapi import APIRouter

from backend.models import UserSetting
from backend.utils.jwt import decode_jwt
from utils.globals import USER_DB

router = APIRouter()
logger = logging.getLogger("ronnia-web")


@router.get("/user_details", summary='Gets registered user details from database')
async def get_user_details(jwt_token: str):
    """
        Get registered user details from database:
        - **jwt_token**: JWT token of the current user
    """
    user_data_dict = decode_jwt(jwt_token)
    user_id = user_data_dict['user_id']
    user_settings = await USER_DB.select_all_settings_by_user_id(user_id)
    excluded_users = await USER_DB.select_excluded_users_by_user_id(user_id)
    user_data_dict['excluded_users'] = excluded_users
    user_data_dict['settings'] = user_settings

    return user_data_dict


@router.post('/save_user_settings', summary="Save user settings")
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
    excluded_users = payload.excluded_users
    jwt_token = payload.jwt_token
    user_data = decode_jwt(jwt_token=jwt_token)
    user_id = user_data['user_id']
    for setting in settings:
        if setting.type == 'toggle' or setting.type == 'value':
            await USER_DB.set_setting(user_id=user_id, setting_key=setting.key, new_value=setting.value)
        elif setting.type == 'range':
            if setting.range_end == 10:
                setting.range_end = -1
            await USER_DB.set_range_setting(user_id=user_id, setting_key=setting.key, range_low=setting.range_start,
                                            range_high=setting.range_end)

    await USER_DB.set_excluded_users(user_id=user_id, excluded_users=excluded_users)
    return
