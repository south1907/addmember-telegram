import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime
import time
from typing import List, Dict, Any, Optional

from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from telethon.tl.types import InputPeerUser

from utils import *

# Configure logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config() -> Dict[str, Any]:
	"""Load and validate configuration."""
	try:
		with open('config.json', 'r', encoding='utf-8') as f:
			config = json.loads(f.read())
		
		required_fields = ['accounts', 'group_source', 'group_target', 'api_id', 'api_hash']
		for field in required_fields:
			if field not in config:
				raise ValueError(f"Missing required config field: {field}")
		
		return config
	except Exception as e:
		logging.error(f"Failed to load config: {e}")
		sys.exit(1)

def initialize_clients(config: Dict[str, Any]) -> List[Dict[str, Any]]:
	"""Initialize Telegram clients and join target group."""
	clients = []
	root_path = Path(__file__).parent
	session_path = root_path / 'session'
	
	for phone in config['accounts']:
		try:
			client = TelegramClient(
				str(session_path / phone),
				int(config['api_id']),
				config['api_hash']
			)
			
			client.connect()
			
			if not client.is_user_authorized():
				logging.warning(f"Login failed for account: {phone}")
				continue
				
			# Join target group
			client(JoinChannelRequest(config['group_target']))
			entity_group = client.get_entity(config['group_target'])
			
			clients.append({
				'phone': phone,
				'client': client,
				'group_target': entity_group
			})
			
		except Exception as e:
			logging.error(f"Failed to initialize client for {phone}: {e}")
			continue
			
	if not clients:
		logging.error("No valid clients initialized")
		sys.exit(1)
		
	return clients

def process_user(
	user: Dict[str, Any],
	current_client: Dict[str, Any],
	list_id_processed: List[str],
	path_file_log: Path
) -> str:
	"""Process a single user and return the status."""
	if current_client['phone'] not in user:
		return 'SKIP_NO_INFO'
		
	try:
		user_to_add = InputPeerUser(
			int(user[current_client['phone']]['user_id']),
			int(user[current_client['phone']]['access_hash'])
		)
		status = add_member_to_group(
			current_client['client'],
			current_client['group_target'],
			user_to_add
		)
		
		list_id_processed.append(str(user['user_id']))
		write_log_processed(path_file_log, list_id_processed)
		
		return status
	except Exception as e:
		logging.error(f"Error processing user {user['user_id']}: {e}")
		return 'ERROR_OTHER'

def main():
	config = load_config()
	clients = initialize_clients(config)
	
	# Setup paths
	root_path = Path(__file__).parent
	data_path = root_path / 'data' / str(config['group_source'])
	log_path = root_path / 'data-log' / f"{config['group_target']}.txt"
	
	# Load data
	users = read_data_member(data_path)
	list_id_processed = read_log_processed(log_path)
	
	# Configuration
	total_time_in_round = 120
	total_user_big_sleep = 35
	time_big_sleep = 7200
	from_date_active = config.get('from_date_active', '19700101')
	
	# Initialize counters
	count_added = 0
	total_count_added = 0
	start_time = datetime.now()
	
	# Get existing users in target group
	list_user_id_in_target = get_list_user_id_of_group(clients[0]['client'], config['group_target'])
	
	# Main processing loop
	for i, user in enumerate(users):
		if count_added >= (total_user_big_sleep * len(clients)):
			logging.info("Big sleep, sleeping 2 hours")
			for client in clients:
				client['client'].disconnect()
			time.sleep(time_big_sleep)
			for client in clients:
				client['client'].connect()
			count_added = 0
			
		# Skip conditions
		if (user['date_online'] != 'online' and user['date_online'] < from_date_active):
			logging.info(f"User {user['user_id']} is overdue")
			continue
			
		if user['user_id'] in list_user_id_in_target:
			logging.info(f"User {user['user_id']} already in target group")
			continue
			
		if str(user['user_id']) in list_id_processed:
			logging.info(f"User {user['user_id']} already processed")
			continue
			
		# Process user
		current_client = clients[count_added % len(clients)]
		status = process_user(user, current_client, list_id_processed, log_path)
		
		if status == 'SUCCESS':
			count_added += 1
			total_count_added += 1
			time.sleep(total_time_in_round / len(clients))
		elif status in ('FLOOD', 'FLOOD_WAIT'):
			logging.warning(f"Flood detected, removing client: {current_client['phone']}")
			current_client['client'].disconnect()
			clients.remove(current_client)
			if not clients:
				logging.error("No more clients available")
				break
		elif status == 'ERROR_OTHER':
			time.sleep(total_time_in_round / len(clients))
			
	# Cleanup
	for client in clients:
		client['client'].disconnect()
		
	end_time = datetime.now()
	logging.info(f"Added {total_count_added} members in {end_time - start_time}")

if __name__ == "__main__":
	main()
