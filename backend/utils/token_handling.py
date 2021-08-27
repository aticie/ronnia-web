import json

import aiohttp


async def get_token(token_endpoint, parameters):
    async with aiohttp.ClientSession() as session:
        async with session.post(token_endpoint, data=parameters) as resp:
            token_result = json.loads(await resp.read())

    return token_result
