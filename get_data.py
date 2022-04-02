from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
import json
from datetime import datetime, timedelta

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
    groups = []

    query = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
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
    with open('data/group/' + phone + '.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def get_data_user(client, group):
    group_id = str(group.id)
    print(group_id)

    while_condition = True
    my_filter = ChannelParticipantsSearch('')
    offset = 0
    all_participants = []
    
    while while_condition:
        participants = client(GetParticipantsRequest(channel=group,  offset= offset, filter = my_filter, limit=200, hash=0))
        
        all_participants.extend(participants.users)
        offset += len(participants.users)
        
        print(len(participants.users))
        
        if len(participants.users) < 1 :
            while_condition = False
            
    results = []
    today = datetime.now()
    last_week = today + timedelta(days=-7)
    last_month = today + timedelta(days=-30)
    path_file = 'data/user/' + phone + "_" + group_id + '.json'

    for user in all_participants:
        # print(user)
        # print(type(user.status))
        try:
            if isinstance(user.status, UserStatusRecently):
                date_online_str = 'online'
            else:
                if isinstance(user.status, UserStatusLastMonth):
                    date_online = last_month
                if isinstance(user.status, UserStatusLastWeek):
                    date_online = last_week
                if isinstance(user.status, UserStatusOffline):
                    date_online = user.status.was_online

                date_online_str = date_online.strftime("%Y%m%d")
            tmp = {
                'user_id': str(user.id),
                'access_hash': str(user.access_hash),
                'username': str(user.username),
                "date_online": date_online_str
            }
            results.append(tmp)
        except:
            print("Error get user")
    with open(path_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

accounts = config['accounts']

folder_session = 'session/'

for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    print(phone)
    get_group(phone, api_id, api_hash)
