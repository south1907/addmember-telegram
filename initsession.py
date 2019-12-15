from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events

logging.basicConfig(level=logging.WARNING)

api_id = 11007498
api_hash = '57c6f3c72c2f21676d53be2e1deab3aa'
phone = '+84976081803'


client = TelegramClient(phone, api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=('116.203.2.245', 1337, 'dd81b667f85e7e5d358de3b8e4ade6302f'))

client.start()
if client.is_user_authorized():
	print('dang nhap thanh cong')
else:
	print('dang nhap khong thanh cong')
client.disconnect()