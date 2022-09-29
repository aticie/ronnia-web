import logging
import os
from typing import Optional

from backend.utils.discord import DiscordPoster

logger = logging.getLogger('ronnia-web')


async def send_alert_to_discord(title: Optional[str], description: Optional[str]):
    dp = DiscordPoster(os.getenv("DISCORD_BOT_TOKEN"), os.getenv("DISCORD_LOG_CHANNEL_ID"))
    await dp.post(title, description)
