# addmember-telegram
Add member auto to telegram group

Note: need about 20 accounts to run
### init session
run init session to create session for on phone

+ create app in https://my.telegram.org/apps and have api_id, api_hash
+ backup session to somewhere

### create phone.txt

create phone.txt have format same phone.example.txt
phone;api_id;api_hash

### getdata.py

+ get groups, users in group and save folder data

### addmember.py
change id group source, target, base on file data/group/+84....csv (need upgrade in the future)

group_target_id = 1331409327
group_source_id = 1166894130

