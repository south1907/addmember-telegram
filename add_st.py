import sys
import os
import json
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon import sync, TelegramClient, events

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
root_path = os.path.dirname(os.path.abspath(__file__))
accounts = config['accounts']
print("Total account: " + str(len(accounts)))
folder_session = 'session/'

# group target
group_target_id = config['group_target']
# group source
group_source_id = config['group_source']
group_source_username = config['group_source_username']
group_target_username = config['group_target_username']


clients = []
for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    try:
        client = TelegramClient(folder_session + phone, api_id, api_hash)
        client.connect()
        client(JoinChannelRequest(group_source_username))
        client(JoinChannelRequest(group_target_username))
        print(phone + " added source and target group")
        
    except:
        try:
            client(ImportChatInviteRequest(group_source_username))
        except:
         print(f"Add All Of Ur Account to Source Group And Run `python get_data.py` ")

        

    if client.is_user_authorized():
        print(bcolors.OKGREEN + phone + ' login success' + bcolors.ENDC)
        clients.append({
            'phone': phone,
            'client': client
        })
        client.disconnect()
    else:
        print(bcolors.FAIL + phone + ' login fail' + bcolors.ENDC)
     
exec(open("get_data.py").read())
with open(root_path + '/current_count.txt') as f:
    count = f.read()
    with open(root_path + '/current_count.txt.bakup', 'w') as g:
        g.write(str(count))
with open(root_path + '/current_count.txt', 'w') as h:
    i = 0
    h.write(str(i))

    
        
