from typing import List, Union

from pydantic import BaseModel


class Setting(BaseModel):
    id: int
    key: str
    default_value: int
    description: str
    type: str
    value: int
    pass


class RangeSetting(BaseModel):
    id: int
    key: str
    default_low: float
    default_high: float
    description: str
    type: str
    range_start: float
    range_end: float
    pass


class UserSetting(BaseModel):
    jwt_token: str
    settings: List[Union[Setting, RangeSetting]]
    pass
