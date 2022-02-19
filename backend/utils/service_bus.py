import json
import logging
import os

from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from fastapi import HTTPException

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
                raise HTTPException(status_code=503, detail="We received your signup request, but we couldn't "
                                                            "process it. Please try again later.")
            reply_message = reply_messages[0]
            logger.info(f"Received reply message from service bus: {str(reply_message)}")
            await receiver.complete_message(reply_message)

    return json.loads(str(reply_message))
