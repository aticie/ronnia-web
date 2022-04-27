from utils.globals import STATISTICS_DB

from fastapi import APIRouter

router = APIRouter(prefix='/beatmaps')


@router.get("/most_requested", summary='Gets the most requested 5 beatmaps')
async def get_most_requested():
    return await STATISTICS_DB.get_top_n_beatmaps_this_week()


@router.get("/latest_channel", summary='Gets the latest requested beatmaps on a channel')
async def get_latest_channel_beatmaps(twitch_username: str):
    return await STATISTICS_DB.get_latest_beatmaps_of_user(twitch_username=twitch_username)


@router.get("/most_channel", summary='Gets the most requested beatmaps on a channel')
async def get_most_beatmaps_by_channel(twitch_username: str):
    return await STATISTICS_DB.get_top_n_beatmaps_by_channel(twitch_username=twitch_username)


@router.get("/most_requesters", summary='Gets the count of requested beatmaps of all user')
async def get_most_requesters():
    return await STATISTICS_DB.get_count_requested_by_user()


@router.get("/requesters_on_channel", summary='Gets the top 5 requesters on a channel')
async def get_most_requesters_on_channel(twitch_username: str):
    return await STATISTICS_DB.get_most_requesters_on_channel(twitch_username)
