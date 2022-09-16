import os
import json
import time

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

accounts = config['accounts']
print("Total account: " + str(len(accounts)))
folder_session = 'session/'

# login
clients = []
for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    clients.append({
         'phone': phone
        })

# group target
group_target_id = config['group_target']
# group source
group_source_id = config['group_source']
root_path = os.path.abspath(os.curdir)

# filter clients


def filterus():
    for my_client in clients:
        phone = my_client['phone']

        path_group = root_path + '/data/group/' + phone + '.json'
        path_group2 = root_path + '/data/filteruser/' + \
            phone + "_" + str(group_source_id) + '.json'
        if os.path.isfile(path_group):
            json2 = root_path + '/data/user/' + \
                phone + "_" + str(group_source_id) + '.json'
            json1 = root_path + '/data/user/' + \
                phone + "_" + str(group_target_id) + '.json'
            try: 
                with open(json1) as f:
                    json11 = json.loads(f.read())
                with open(json2) as b:
                    json22 = json.loads(b.read())

                newjson = [user for user in json22 if not any(
                    user["user_id"] == other["user_id"] for other in json11)]
                with open(path_group2, "w") as f:
                    json.dump(newjson, f, ensure_ascii=False, indent=4)
                    
                print("Filter process done for :" + phone)
            #disconect

            except:
                print("U might be banned from Source or Target with this number " + phone)
                continue
        else:
            #disconect
            time.sleep(2)


filterus()
