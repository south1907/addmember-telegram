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
path_current_count = root_path + '/current_count.txt'

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
path_file = folder_data + str(group_source) + '.json'
with open(path_file, 'r', encoding='utf-8') as f:
	users = json.loads(f.read())

try:
	with open(path_current_count, 'r') as f:
		previous_count = int(f.read())
except:
	previous_count = 0

# date_online_from
from_date_active = '19700101'
if 'from_date_active' in config:
	from_date_active = config['from_date_active']

i = previous_count # index loop user
count_added = 0 # count added success (in 1 big round)
total_count_added = 0 # total count added success

assert len(accounts) > 0

def handler(signum, frame):
	msg = " Do you really want to exit? y/n\n"
	print(msg, end="", flush=True)
	res = readchar.readchar()
	if res == 'y':
		for cli in clients:
			cli['client'].disconnect()

		update_count(path_current_count, i)
		sys.exit()
	else:
		print("", end="\r", flush=True)
		print(" " * len(msg), end="", flush=True)  # clear the printed line
		print("    ", end="\r", flush=True)

if platform.system() == 'Windows':
	signal.signal(signal.SIGTERM, handler)
	signal.signal(signal.SIGINT, handler)
else:
	signal.signal(signal.SIGINT, handler)
	signal.signal(signal.SIGTSTP, handler)

# init TelegramClient 
for phone in accounts:
	client = TelegramClient(folder_session + phone, api_id, api_hash)

	client.connect()

	if client.is_user_authorized():
		# join group
		client(JoinChannelRequest(group_target))
		clients.append({
			'phone': phone,
			'client': client
		})
	else:
		logging.info(phone + ' login fail')

assert len(clients) > 0

# use first client to get entity_group_target
entity_group_target = clients[0]['client'].get_entity(group_target)

total_user = len(users)
total_client = len(clients)

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
		logging.info('User ' + user['user_id'] + ' has time active: ' +
			  user['date_online'] + ' is overdue')
		continue

	
	current_index = count_added % total_client
	current_client = clients[count_added % total_client]

	logging.info('Adding user id: ' + str(user['user_id']))
	user_to_add = InputPeerUser(int(user['user_id']), int(user['access_hash']))
	status_add = add_member_to_group(current_client['client'], entity_group_target, user_to_add)

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

	if status_add == 'USER_PRIVACY' or status_add == 'ERROR_OTHER':
		logging.info(status_add + ', skip user')


	# if status_add is not FLOOD and FLOOD_WAIT
	if status_add != 'FLOOD' and status_add != 'FLOOD_WAIT':
		i += 1

	# check client empty
	if total_client == 0:
		logging.info('END: accounts is empty')
		break

update_count(path_current_count, i)

for cli in clients:
	cli['client'].disconnect()
	time.sleep(2)
end_time = datetime.now()

logging.info("added: " + str(total_count_added))
logging.info("total time: " + str(end_time - start_time))
