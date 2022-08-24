import json
import os

n = int(input("How many account U want to as worker: "))

root_path = os.path.abspath(os.curdir)
pathc = root_path + '/config.json'

if os.path.exists(pathc):
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
        
    makeconfig = [{"phone": input("phone Number With +Country code: "), "api_id": input("api_id Get from my.telegram.org: "), "api_hash": input("api_hash Get from my.telegram.org: ")} for _ in range(n)]
    config["accounts"].extend(makeconfig)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
        
else:
    makeconfig = {"group_source": input("group_source: "),  "group_target": input("group_target: "), "group_source_username": input("group_source_username: "), "from_date_active": "20201114", "accounts": [{"phone": input("phone Number With +Country code: "), "api_id": input("api_id Get from my.telegram.org: "), "api_hash": input("api_hash Get from my.telegram.org: ")} for _ in range(n)] }
    with open('config.json', 'w') as f:
        json.dump(makeconfig, f, indent=4)