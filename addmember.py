from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError
import random
import time
import traceback
import datetime
import os.path

start_time = datetime.datetime.now()
logging.basicConfig(level=logging.WARNING)

with open('phone.txt') as f:
	data_client = f.read().split("\n")

clients = []

# group target
group_target_id = 1201324407

# group source
group_source_id = 1166894130

for row_client in data_client:
	split_row_client = row_client.split(";")
	if(split_row_client.__len__() > 2):
		phone = split_row_client[0]
		api_id = int(split_row_client[1])
		api_hash = split_row_client[2]

		client = TelegramClient(phone, api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=('116.203.2.245', 1337, 'dd81b667f85e7e5d358de3b8e4ade6302f'))

		client.connect()
		clients.append({
			'phone': phone,
			'client': client
		})

for my_client in clients:
	phone = my_client['phone']
	if os.path.isfile('data/group/' + phone + '.csv'):
		# TODO read group to get group_access_hash
		with open('data/group/' + phone + '.csv', encoding='utf-8') as f:
			groups = [x.split(";") for x in f.read().split("\n")]

		group_access_hash = None
		for group in groups:
			# print(group)
			if(group_target_id == int(group[0])):
				group_access_hash = int(group[1])
				print('bang cmnr')
				break

		target_group_entity = InputPeerChannel(group_target_id, group_access_hash)

		if os.path.isfile('data/user/' + phone + "_" + str(group_source_id) + '.csv'):
			# add target_group_entity key value
			my_client['target_group_entity'] = target_group_entity
			# TODO read user, add users list
			with open('data/user/' + phone + "_" + str(group_source_id) + '.csv', encoding='utf-8') as f:
				users = [x.split(";") for x in f.read().split("\n")]
				my_client['users'] = users
		else:
			clients.remove(my_client)

	else:
		clients.remove(my_client)

total_client = clients.__len__()

previous_count = 0
with open('current_count.txt') as f:
	previous_count = int(f.read())

count_add = 0
if (total_client > 0):
	total_user = clients[0]['users'].__len__()
	print(total_client)

	for i in range(0, total_user):
		
		current_index = count_add % total_client
		print("current_index: " + str(current_index))
		current_client = clients[current_index]
		client = current_client['client']
		user = current_client['users'][i]
		target_group_entity = current_client['target_group_entity']

		# previous run
		if(i < previous_count):
			continue

		# count_add if added 50 user
		if count_add % 50 == 49:
			print('sleep: ' + str(900/total_client))
			time.sleep(900/total_client)

		try:
			if(user.__len__() > 1):
				tmp_user = {
					'id': int(user[0]),
					'access_hash': int(user[1])
				}
					
				user_to_add = InputPeerUser(tmp_user['id'], tmp_user['access_hash'])
				client(InviteToChannelRequest(target_group_entity,[user_to_add]))
				print("Add thanh cong")
				count_add += 1
				print('sleep: ' + str(60/total_client))
				time.sleep(60/total_client)
			
		except PeerFloodError as e:
			print("Error Fooling cmnr")

			with open('current_count.txt', 'w') as g:
				g.write(str(i))
				g.close()
			break
		except UserPrivacyRestrictedError:
			print("Error Privacy")
		except:
			print("Error other")
			traceback.print_exc()

		# if(count_add > 3):
		# 	break


end_time = datetime.datetime.now()
print("total: " + str(count_add))
print("total time: " + str(end_time - start_time))