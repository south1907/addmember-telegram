#!/usr/bin/env python3

import json
import logging
import time

from telethon import sync, TelegramClient, events
from telethon import TelegramClient, connection

from utils import *

with open('config.json', 'r') as f:
    config = json.loads(f.read())

logging.basicConfig(level=logging.WARNING)

accounts = config['accounts']

folder_session = 'session/'

api_id = int(config['api_id'])
api_hash = config['api_hash']
for phone in accounts:
    logging.info(phone)

    client = TelegramClient(folder_session + phone, api_id, api_hash)
    client.start()
    if client.is_user_authorized():
        time.sleep(2)
        logging.info('Login success')

    else:
        logging.info('Login fail')
    client.disconnect()
