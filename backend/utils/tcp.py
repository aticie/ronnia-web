import asyncio
import json


async def signup_user_over_tcp_async(signup_data: dict):
    reader, writer = await asyncio.open_connection(host='localhost', port=9999)
    writer.write(json.dumps(signup_data).encode('utf-8'))
    await writer.drain()

    result = await reader.read(4096)

    writer.close()
    await writer.wait_closed()

    return json.loads(result.decode('utf-8'))

