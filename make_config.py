import json
import os

root_path = os.path.dirname(os.path.abspath(__file__))
with open(root_path + '/config.json') as f:
    data = f.read()
    with open(root_path + '/config.json.bakup', 'w') as g:
        g.write(str(data))

n = int(input("How many account U ass worker: "))
makeconfig = {"group_source": input("group_source: "),  "group_target": input("group_target: "), "group_source_username": input("group_source_username: "), "from_date_active": "20201114", "accounts": [{"phone": input("phone Number With +Country code: "), "api_id": input("api_id Get from my.telegram.org: "), "api_hash": input("api_hash Get from my.telegram.org: ")} for _ in range(n)] }

with open('config.json', 'w') as f:
    json.dump(makeconfig, f, indent=4)