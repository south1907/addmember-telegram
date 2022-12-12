import sys
import os
import json
import platform
import signal
import readchar
from datetime import datetime
import time

from telethon.tl.functions.channels import JoinChannelRequest
from telethon import sync, TelegramClient, events
from telethon.tl.types import InputPeerUser

from utils import *


with open('config.json', 'r', encoding='utf-8') as f:
	config = json.loads(f.read())

root_path = os.path.dirname(os.path.abspath(__file__))
folder_session = root_path + '/session/'
folder_data = root_path + '/data/'

accounts = config['accounts']

# start_time
start_time = datetime.now()

group_source = config['group_source']
group_target = config['group_target']
api_id = int(config['api_id'])
api_hash = config['api_hash']
total_time_in_round = 120
total_user_big_sleep = 35
time_big_sleep = 7200

# list client
clients = []

# data user need add to group
path_folder_file = folder_data + '/' + str(group_source)
users = read_data_member(path_folder_file)

# date_online_from
from_date_active = '19700101'
if 'from_date_active' in config:
	from_date_active = config['from_date_active']

i = 0 # alway from 0 because have logic check user_id from target group
count_added = 0 # count added success (in 1 big round)
total_count_added = 0 # total count added success

assert len(accounts) > 0

# init TelegramClient 
for phone in accounts:
	client = TelegramClient(folder_session + phone, api_id, api_hash)

	client.connect()

	if client.is_user_authorized():
		# join group
		client(JoinChannelRequest(group_target))
		entity_group = client.get_entity(group_target)
		clients.append({
			'phone': phone,
			'client': client,
			'group_target': entity_group
		})
	else:
		logging.info(phone + ' login fail')

total_user = len(users)
total_client = len(clients)
logging.info('total member need to add : ' + str(total_user))
logging.info('total account run: ' + str(total_client))

# use first client to get list user_id of target group
list_user_id_in_target = get_list_user_id_of_group(clients[0]['client'], group_target)

while i < total_user:

	# count_added if added 35 user
	if count_added >= (total_user_big_sleep * total_client):
		logging.info('Big sleep, sleep 2 hours')
		for cli in clients:
			cli['client'].disconnect()
			time.sleep(2)
		time.sleep(time_big_sleep)
		for cli in clients:
			cli['client'].connect()
			time.sleep(2)
		count_added = 0 # reset

	logging.info('current index user: ' + str(i))
	user = users[i]
	# not add user overdue (not online far away)
	if user['date_online'] != 'online' and user['date_online'] < from_date_active:
		i += 1
		logging.info('User ' + str(user['user_id']) + ' has time active: ' +
			  user['date_online'] + ' is overdue')
		continue

	if user['user_id'] in list_user_id_in_target:
		i += 1
		logging.info('User ' + str(user['user_id']) + ' in target group, not add')
		continue
	
	current_index = count_added % total_client
	current_client = clients[count_added % total_client]

	logging.info('Adding user id: ' + str(user['user_id']))

	if current_client['phone'] not in user:
		i += 1
		logging.info('ignore user id: ' + str(user['user_id']) + ' by not have information for client: ' + current_client['phone'])
		continue


	user_to_add = InputPeerUser(int(user[current_client['phone']]['user_id']), int(user[current_client['phone']]['access_hash']))
	status_add = add_member_to_group(current_client['client'], current_client['group_target'], user_to_add)

	logging.info("status_add: " + status_add)
	if status_add == 'SUCCESS':
		logging.info('Added member ' + str(user['user_id']) + ' successfully ;-)')	
		logging.info('sleep: ' + str(total_time_in_round / total_client))
		time.sleep(total_time_in_round / total_client)
		count_added += 1
		total_count_added += 1

	if status_add == 'FLOOD' or status_add == 'FLOOD_WAIT':
		logging.info('FLOOD, remove client: ' + current_client['phone'])
		current_client['client'].disconnect()
		clients.remove(current_client)

		# cal total_client
		total_client = len(clients)

	if status_add == 'USER_PRIVACY':
		logging.info(status_add + ', skip user')

	if status_add == 'ERROR_OTHER':
		logging.info(status_add + ', skip user')
		time.sleep(total_time_in_round / total_client)


	# if status_add is not FLOOD and FLOOD_WAIT
	if status_add != 'FLOOD' and status_add != 'FLOOD_WAIT':
		i += 1

	# check client empty
	if total_client == 0:
		logging.info('END: accounts is empty')
		break

for cli in clients:
	cli['client'].disconnect()
	time.sleep(2)
end_time = datetime.now()

logging.info("added: " + str(total_count_added))
logging.info("total time: " + str(end_time - start_time))
