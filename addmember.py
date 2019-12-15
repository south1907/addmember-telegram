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
import os

root_path = os.path.dirname(os.path.abspath(__file__))
print(root_path)

start_time = datetime.datetime.now()
print(start_time)
logging.basicConfig(level=logging.WARNING)

with open(root_path + '/phone.txt') as f:
	data_client = f.read().split("\n")
print(data_client)
clients = []

#TODO: change file config
# group target
group_target_id = 1331409327

# group source
group_source_id = 1166894130

for row_client in data_client:
	split_row_client = row_client.split(";")
	if(split_row_client.__len__() > 2):

		# folder save session
		phone = split_row_client[0]
		api_id = int(split_row_client[1])
		api_hash = split_row_client[2]
		client = TelegramClient(root_path + "/" + phone, api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=('116.203.2.245', 1337, 'dd81b667f85e7e5d358de3b8e4ade6302f'))

		client.connect()

		if (client.is_user_authorized()):
			print('dang nhap thanh cong')
			clients.append({
				'phone': phone,
				'client': client
			})
		else:
			print('dang nhap khong thanh cong')

print(clients.__len__())
for my_client in clients:
	phone = my_client['phone']
	print(root_path + '/data/group/' + phone + '.csv')
	if os.path.isfile(root_path + '/data/group/' + phone + '.csv'):
		print('vaoo')
		# TODO read group to get group_access_hash
		with open(root_path + '/data/group/' + phone + '.csv', encoding='utf-8') as f:
			groups = [x.split(";") for x in f.read().split("\n")]

		group_access_hash = None
		for group in groups:
			print(group)
			if(group.__len__() > 2):
				if(group_target_id == int(group[0])):
					group_access_hash = int(group[1])
					print('bang cmnr')
					break

		target_group_entity = InputPeerChannel(group_target_id, group_access_hash)

		if os.path.isfile(root_path + '/data/user/' + phone + "_" + str(group_source_id) + '.csv'):
			# add target_group_entity key value
			my_client['target_group_entity'] = target_group_entity
			# TODO read user, add users list
			with open(root_path + '/data/user/' + phone + "_" + str(group_source_id) + '.csv', encoding='utf-8') as f:
				users = [x.split(";") for x in f.read().split("\n")]
				my_client['users'] = users
		else:
			print('khooeoe 2')
			clients.remove(my_client)

	else:
		print('khooeoe')
		clients.remove(my_client)

total_client = clients.__len__()

previous_count = 0
with open(root_path + '/current_count.txt') as f:
	previous_count = int(f.read())

count_add = 0
if (total_client > 0):
	total_user = clients[0]['users'].__len__()
	print(total_client)

	i = 0
	while i < total_user:
		print(i)
		current_index = count_add % total_client
		print("current_index: " + str(current_index))
		current_client = clients[current_index]
		client = current_client['client']
		user = current_client['users'][i]
		target_group_entity = current_client['target_group_entity']

		# previous run
		if(i < previous_count):
			i += 1
			continue

		# count_add if added 35 user
		if count_add % (35 * total_client) == (35 * total_client - 1):
			print('Thoat ra sau 15 phut chay tiep')
			with open(root_path + '/current_count.txt', 'w') as g:
				g.write(str(i))
				g.close()
			break

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
				print('sleep: ' + str(120/total_client))
				time.sleep(120/total_client)
			
		except PeerFloodError as e:
			print("Error Fooling cmnr")
			traceback.print_exc()
			print("remove client: " + current_client['phone'])
			client.disconnect()
			clients.remove(current_client)
			total_client = clients.__len__()
			print("remain client: " + str(total_client))
			if(total_client == 0):

				with open(root_path + '/current_count.txt', 'w') as g:
					g.write(str(i))
					g.close()
				break

			# not increate i
			continue
		except UserPrivacyRestrictedError:
			print("Error Privacy")
		except:
			print("Error other")
			traceback.print_exc()
			# break

		i += 1
		# if(count_add > 3):
		# 	break

print("disconnect")
for cli in clients:
	cli['client'].disconnect()
end_time = datetime.datetime.now()
print("total: " + str(count_add))
print("total time: " + str(end_time - start_time))
