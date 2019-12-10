from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

logging.basicConfig(level=logging.WARNING)

with open('phone.txt') as f:
	data_client = f.read().split("\n")

for row_client in data_client:
	split_row_client = row_client.split(";")
	if(split_row_client.__len__() > 2):
		phone = split_row_client[0]
		api_id = int(split_row_client[1])
		api_hash = split_row_client[2]

		client = TelegramClient(phone, api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=('116.203.2.245', 1337, 'dd81b667f85e7e5d358de3b8e4ade6302f'))

		client.connect()
		if not client.is_user_authorized():
			print('dang nhap khong thanh cong')
		else:
			print('getting data ' + phone)
			chats = []
			last_date = None
			chunk_size = 200
			groups=[]
			 
			result = client(GetDialogsRequest(
						 offset_date=last_date,
						 offset_id=0,
						 offset_peer=InputPeerEmpty(),
						 limit=chunk_size,
						 hash = 0
					 ))
			chats.extend(result.chats)
			for chat in chats:
				try:
					if chat.megagroup is not None and chat.access_hash is not None:
						groups.append(chat)
				except:
					continue

			str_group = ''
			for group in groups:

				try:
					group_id = str(group.id)
					access_hash = str(group.access_hash)
					title = str(group.title)

					row_group = group_id + ";" + access_hash + ";" + title + "\n"

					str_group += row_group

					if (group.megagroup == True):
						print(group_id)
						all_participants = []
						all_participants = client.get_participants(group, aggressive=True)
						result = ''
						for user in all_participants:

							user_id = str(user.id)
							access_hash = str(user.access_hash)
							username = str(user.username)
							fullname = str(user.first_name) + " " + str(user.last_name)

							row = user_id + ";" + access_hash + ";" + username + ";" + fullname + "\n"

							result += row
						with open('data/user/' + phone + "_" + str(group_id) +'.csv', 'w', encoding='utf-8') as f:
							f.write(result)
							f.close()
				except Exception as e:
					print('loi lay user')
				

			with open('data/group/' + phone + '.csv', 'w') as g:
				g.write(str_group)
				g.close()