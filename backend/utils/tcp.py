from multiprocessing.connection import Client
from queue import Queue
from typing import Optional


def signup_user_over_tcp(signup_data: dict, message_queue: Queue, authkey: Optional[str] = None):
    if isinstance(authkey, str):
        authkey = authkey.encode('utf-8')

    with Client(('localhost', 9999), authkey=authkey) as conn:
        conn.send(signup_data)
        result = conn.recv()

    message_queue.put(result)
    return result
