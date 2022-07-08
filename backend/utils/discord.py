import logging
from typing import Optional

import aiohttp

logger = logging.getLogger('ronnia-web')


class DiscordPoster:
    def __init__(self, bot_token: str, channel_id: str):
        self.base_url = 'https://discord.com/api/v10'
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.auth_header = {'Authorization': f'Bot {self.bot_token}'}
        logger.info('Initialized Discord Poster')

    async def post(self, title: Optional[str], description: Optional[str]):
        url = f'{self.base_url}/channels/{self.channel_id}/messages'

        form_params = {'embeds': [self.create_embed(title, description)]}
        async with aiohttp.ClientSession(headers=self.auth_header) as sess:
            async with sess.post(url, json=form_params) as r:
                resp = await r.json()

        print(resp)

    @staticmethod
    def create_embed(title: Optional[str],
                     description: Optional[str]):
        return {"title": title,
                "description": description}
