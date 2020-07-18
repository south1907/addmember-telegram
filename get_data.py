from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import json

logging.basicConfig(level=logging.WARNING)

def get_group(phone, api_id, api_hash):
	folder_session = 'session/'
	client = TelegramClient(folder_session + phone, api_id, api_hash)
	client.connect()
	if not client.is_user_authorized():
		print('Login fail, need to run init_session')
	else:
		get_data_group(client, phone)

def get_data_group(client, phone):
	print('getting data ' + phone)
	chats = []
	last_date = None
	chunk_size = 200
	groups=[]
	 
	query = client(GetDialogsRequest(
				 offset_date=last_date,
				 offset_id=0,
				 offset_peer=InputPeerEmpty(),
				 limit=chunk_size,
				 hash = 0
			 ))
	chats.extend(query.chats)
	for chat in chats:
		try:
			if chat.megagroup is not None and chat.access_hash is not None:
				groups.append(chat)
		except:
			continue

	results = []
	for group in groups:
		try:
			tmp = {
				'group_id': str(group.id),
				'access_hash': str(group.access_hash),
				'title': str(group.title),
			}
			results.append(tmp)
			
			if group.megagroup == True:
				get_data_user(client, group)
		except Exception as e:
			print(e)
			print('error save group')
	with open('data/group/' + phone + '.json', 'w') as f:
		json.dump(results, f, indent=4, ensure_ascii=False)

def get_data_user(client, group):
	group_id = str(group.id)
	print(group_id)

	all_participants = []
	all_participants = client.get_participants(group, aggressive=True)
	results = []
	for user in all_participants:
		tmp = {
			'user_id': str(user.id),
			'access_hash': str(user.access_hash),
			'username': str(user.username)
		}
		results.append(tmp)
	with open('data/user/' + phone + "_" + group_id +'.json', 'w') as f:
		json.dump(results, f, indent=4, ensure_ascii=False)

		
with open('config.json', 'r') as f:
	config = json.loads(f.read())

accounts = config['accounts']

folder_session = 'session/'

for account in accounts:
	api_id = account['api_id']
	api_hash = account['api_hash']
	phone = account['phone']
	print(phone)
	get_group(phone, api_id, api_hash)