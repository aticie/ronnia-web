import json
import os

from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

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
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        message = ServiceBusMessage(json.dumps(signup_data))
        print("Sending signup message to service bus...")
        print(signup_data)
        await sender.send_messages(message)

        receiver = servicebus_client.get_queue_receiver(queue_name=REPLY_QUEUE_NAME)
        return await receiver.receive_messages(max_wait_time=10)
