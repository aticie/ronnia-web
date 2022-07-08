import json
import logging
import os
from typing import Optional

from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from fastapi import HTTPException

from backend.utils.discord import DiscordPoster

logger = logging.getLogger('ronnia-web')

CONNECTION_STR = os.getenv("SERVICE_BUS_CONNECTION_STR")
QUEUE_NAME = 'webserver-signups'
REPLY_QUEUE_NAME = 'webserver-signups-reply'


async def signup_user_over_mq(signup_data: dict):
    """
    Sends a signup request over the MQ.
    :param signup_data: A dictionary containing the signup data.
    :return: The response from the MQ.
    """
    async with ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR) as servicebus_client:
        async with servicebus_client.get_queue_sender(queue_name=QUEUE_NAME) as sender:
            message = ServiceBusMessage(json.dumps(signup_data))
            logger.info("Sending signup message to service bus...")
            logger.info(signup_data)
            await sender.send_messages(message)

        async with servicebus_client.get_queue_receiver(queue_name=REPLY_QUEUE_NAME, max_wait_time=10) as receiver:
            logger.info(f"Waiting for reply from service bus queue {REPLY_QUEUE_NAME}...")
            reply_messages = await receiver.receive_messages(max_message_count=1)
            if len(reply_messages) == 0:
                await send_alert_to_discord(title="Error with sign-up",
                                            description=f"Failed to sign-up user\n"
                                                        f"Twitch: {signup_data['twitch_username']}\n"
                                                        f"osu!: {signup_data['osu_username']}")
                raise HTTPException(status_code=503, detail="We received your signup request, but we couldn't "
                                                            "process it. Please try again later.")
            reply_message = reply_messages[0]
            logger.info(f"Received reply message from service bus: {str(reply_message)}")
            await receiver.complete_message(reply_message)

    return json.loads(str(reply_message))


async def send_alert_to_discord(title: Optional[str], description: Optional[str]):
    dp = DiscordPoster(os.getenv("DISCORD_BOT_TOKEN"), os.getenv("DISCORD_LOG_CHANNEL_ID"))
    await dp.post(title, description)
