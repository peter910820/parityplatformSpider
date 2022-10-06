import requests
import json

CHANNEL_ACCESS_TOKEN = 'C3vEQJqyOWWUyZ8yuIP1lHgYZDEwvbkJCtxugWtjPotN51uYMOJiob0uK/pIhnnWOPPElS/AqRoNk2CVvcyBuXUghvTJ2Vm9ziLocjqqorLedRTCoQUq811DwP+W6wYD9qxazQGiOvDrBAzgP2gE3AdB04t89/1O/w1cDnyilFU='
authorization_token = "Bearer " + CHANNEL_ACCESS_TOKEN 

headers = {"Authorization":authorization_token, "Content-Type":"application/json"}

# body = {
#     "size": {"width": 2500, "height": 843},
#     "selected": "false",
#     "name": "Menu",
#     "chatBarText": "常用功能",
#     "areas":[
#         {
#           "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
#           "action": {"type": "uri", "label": "Official website", "uri": "https://seller.xiapi.shopee.cn/edu/article/976"}
#         },
#         {
#           "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
#           "action": {"type": "message", "text": "開始比價"}
#         },
#         {
#           "bounds": {"x": 1666, "y": 0, "width": 833, "height": 843},
#           "action": {"type": "message", "text": "熱門推薦"}
#         },
#     ]
# }

# re = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',headers=headers,data=json.dumps(body).encode('utf-8'))

# print(re.text)

from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
rich_menu_id = "richmenu-796fcfe96013ec2a1cceb1c1f6d6200d"

# path = "path of your image"

# with open('./richMenuImg/4.png', 'rb') as f:
#     line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)
print(req.text)

rich_menu_list = line_bot_api.get_rich_menu_list()

print(rich_menu_list)