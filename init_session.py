from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
import json

with open('config.json', 'r') as f:
	config = json.loads(f.read())

logging.basicConfig(level=logging.WARNING)

accounts = config['accounts']

folder_session = 'session/'

for account in accounts:
	api_id = account['api_id']
	api_hash = account['api_hash']
	phone = account['phone']
	print(phone)

	client = TelegramClient(folder_session + phone, api_id, api_hash)
	client.start()
	if client.is_user_authorized():
		print('Login success')
	else:
		print('Login fail')
	client.disconnect()