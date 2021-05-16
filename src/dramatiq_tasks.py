import logging
import json
from flask_app import dramatiq


@dramatiq.actor(queue_name='hello')
def websocket_notify(data):
    logging.info(data)
    with open('websocket.txt', 'a') as f:
        f.write(json.dumps(data))


@dramatiq.actor(queue_name='ready')
def email_notify(data):
    logging.info(data)
    with open('email.txt', 'a') as f:
        f.write(json.dumps(data))
