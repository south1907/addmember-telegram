import json
from pathlib import Path


def main():
    config_path = Path("config.json")  # relative path
    # config_path = Path("config.json").resolve()  # absolute path
    #   alternatively:
    # cwd = Path.cwd()  # current working directory
    # config_path = cwd.joinpath("config.json")
    #   or:
    # config_path = cwd / "config.json"

    n = int(input("How many accounts do you want to make for workers: "))

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
    else:
        config = {
            "group_source": input("group_source: "),
            "group_target": input("group_target: "),
            "group_source_username": input("group_source_username: "),
            "from_date_active": "20201114",
            "accounts": []
        }

    for _ in range(n):
        new_account = {
            "phone": input("phone Number With +Country code: "),
            "api_id": input("api_id Get from my.telegram.org: "),
            "api_hash": input("api_hash Get from my.telegram.org: ")
        }
        config["accounts"].append(new_account)

    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)


if __name__ == '__main__':
    main()
