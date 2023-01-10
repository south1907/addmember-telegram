import sys
import os
import json
from telethon import sync, TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
import traceback
import logging

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

def get_member_by_group_username(client, group_username):

	"""
	:param client: TelegramClient
	:param group_username: username's group
	:return: list telethon.tl.types.User

	Get all member of group by group username
	"""
	all_data = [] # list telethon.tl.types.User
	
	entity = client.get_entity(group_username)
	limit = 200
	my_filter = ChannelParticipantsSearch('')

	i = 0
	while True:
		offset = limit * i
		user_list = client(GetParticipantsRequest(entity, my_filter, offset=offset, limit=limit, hash=0))

		if not user_list.users:
			logging.info('get member done')
			break
		
		all_data.extend(user_list.users)

		i += 1

	return all_data

def get_list_user_id_of_group(client, group_username):

	"""
	:param client: TelegramClient
	:param group_username: username's group
	:return: list user_id

	Get list user_id of group by group username
	"""
	all_data = get_member_by_group_username(client, group_username)
	all_data_id = [] # list user_id
	for item in all_data:
		all_data_id.append(item.id)

	return all_data_id
	

def get_member_by_group_id(client, group_id):

	"""
	:param client: TelegramClient
	:param group_username: id's group
	:return: list telethon.tl.types.User
  
	Get all member of group by group id
	"""

	entity = client.get_entity(group_id)
	return client.get_participants(entity=entity)

def add_member_to_group(client, group_entity, user):

	"""
	:param client: TelegramClient
	:param group_entity: entity group
	:param user: InputPeerUser
	:return: string - SUCCESS, FLOOD, FLOOD_WAIT, USER_PRIVACY, ERROR_OTHER

	add one member to group
	"""
	
	result = 'SUCCESS'
	try:
		client(InviteToChannelRequest(
			group_entity,
			[user]
		))
	except PeerFloodError as e:
		logging.error("Error PeerFloodError")
		traceback.print_exc()
		result = 'FLOOD'
	except FloodWaitError as e:
		logging.error("Error FloodWaitError")
		traceback.print_exc()
		result = 'FLOOD_WAIT'
	except UserPrivacyRestrictedError:
		logging.error("Error UserPrivacyRestrictedError")
		result = 'USER_PRIVACY'
	except BaseException:
		logging.error("Error other")
		traceback.print_exc()
		result = 'ERROR_OTHER'

	return result

def update_count(path, current_index):
	"""
	:param path: path
	:param current_index: current_index
	:return: void

	"""
	with open(path, 'w') as g:
		g.write(str(current_index))
		g.close()

def write_log_processed(path, list_processed):
	"""
	:param path: path
	:param list_processed: list_processed
	:return: void

	"""
	with open(path, 'w') as g:
		g.write('\n'.join(list_processed))
		g.close()

def read_log_processed(path):
	"""
	:param path: path
	:return: list member processed

	"""
	result = []
	try:
		with open(path, encoding='utf-8') as f:
			result = f.read().split('\n')
	except Exception as e:
		pass

	return result

def read_data_member(path_data):
	"""
	:param client: path_data
	:return: list member with user_id, access_hash each phone

	"""
	result = []
	dict_member = {}
	list_file = os.listdir(path_data)

	for file_name in list_file:
		phone = file_name.split('.')[0]
		temp_data_file = []
		with open(path_data + '/' + file_name, encoding='utf-8') as f:
			temp_data_file = json.loads(f.read())

		for item in temp_data_file:
			if item['user_id'] not in dict_member:
				dict_member[item['user_id']] = {
					'user_id': item['user_id'],
					'date_online': item['date_online']
				}

			dict_member[item['user_id']][phone] = {
				'user_id': item['user_id'],
				'access_hash': item['access_hash']
			} 

	for key_map in dict_member:
		result.append(dict_member[key_map])
	
	return result