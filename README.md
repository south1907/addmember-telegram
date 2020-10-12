# addmember-telegram
Use `python 3` to add member from Group A to Group B (migrate member of your group)


## Require
* Environment of python 3 (Linux, Window)
* Need about 20 accounts to run (Avoid block account Telegram)
* Each account need in Source Group and Target Group
* Notice you region phone
* Your group is Supper group

https://www.wikihow.com/Convert-a-Telegram-Group-to-a-Supergroup-on-PC-or-Mac

![Supper group](images/note_tele.png)
![Upgraded Supper group](images/note_tele2.png)

## Guide line

* Step 1: Install package `telethon`
```
pip install telethon
```

* Step 2: Create file config.json
Copy file config.json from config.example.json

```
{
	"group_target": 1398120166, --> id target group
	"group_source": 1490302444, --> id source group
	"accounts": [ --> array account
		{
			"phone": "+84XXXX",
			"api_id": 1234566,
			"api_hash": "57c6f3c72c2f21676d53be2eXXXXXX"
		}
	]
}
```
`group_target` and `group_source`: after run get_data.py and check file in data/group
`accounts`: list account Telegram; each phone, create app in https://my.telegram.org/apps and have api_id, api_hash

* Step 3: After have file `config.json`, run `python init_session.py`, enter phone and the code you received

![Init session](images/step1.png)

* Step 4: run `python get_data.py` to get data of group, data user and save file in folder `data`

![Get data](images/step2.png)
![Data after Get](images/data_step2.png)

```
{
    "user_id": "847587728",
    "access_hash": "2393668282771176567",
    "username": "None"
}
```
One group have one list user (list username), but each account Telegram have list User (difference user_id, access_hash). Use `user_id` and `access_hash` to add member, so you need get list user of each account Telegram.
Note: Use username have also use to add member, but something use not have username

After run get data, check again file in data/group and edit file config to change group_target, group_source, which you want to add.

* Step 5: run `python add_member.py` to add member from `group_source` to `group_target`
Logic: 
	* after add 1 member, sleep 2 minutes
	* each account add 35 member --> sleep 15 minutes
	* Remove account when Exception Flood
	* Break if don't have account

Note: If your account blocked, get link https://web.telegram.org/#/im?p=@SpamBot and chat /start to see time released

![Get data](images/block.png)

Done!

## Ps: 
Because some people interesting my repository create some issue, inbox Telegram. I don't have time to solve it, so I update your script to be good. I will open issue and try to resolved it. But some thing about basic language `python`, please search Internet before create issue! Thanks!
