from wxpy import *
import json
from qqmail import get_qqmail_pop

JSON_FILE = 'config.json'
with open(JSON_FILE) as data_file:    
    data = json.load(data_file)

bot = Bot(console_qr=-2)
tuling = Tuling(api_key=data['api_key'])
groups = []

for name in data['group_name']:
    my_group = bot.groups().search(name)[0]
    groups.append(my_group)

@bot.register(groups, TEXT)
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    else:
        # 回复消息内容和类型
        tuling.do_reply(msg)

user_gmail = data['gmail_account']
pwd_gmail = data['password']

get_qqmail_pop(user_gmail, pwd_gmail)

# 进入 Python 命令行、让程序保持运行
embed()