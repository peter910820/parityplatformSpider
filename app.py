from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os,json,requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi("C3vEQJqyOWWUyZ8yuIP1lHgYZDEwvbkJCtxugWtjPotN51uYMOJiob0uK/pIhnnWOPPElS/AqRoNk2CVvcyBuXUghvTJ2Vm9ziLocjqqorLedRTCoQUq811DwP+W6wYD9qxazQGiOvDrBAzgP2gE3AdB04t89/1O/w1cDnyilFU=")
# Channel Secret
handler = WebhookHandler("c8219d6a121f32f9ae96cc62c5393d45")

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# handle message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '!register':
        msg = []
        msg.append(TextSendMessage(text='歡迎使用註冊功能!請使用下方專用註冊連結填寫資料註冊!'))
        msg.append(TextSendMessage(text=f'https://docs.google.com/forms/d/10_NMvZR9Jl0rga3H76RQfJqkDlBL7VZ4GNqGWqyM7Lk/viewform?entry.1151485071={event.source.user_id}&edit_requested=true'))
        line_bot_api.reply_message(event.reply_token, messages=msg[:5])
    elif event.message.text == '!popular_recommend':
        res = requests.get('https://www.findprice.com.tw/')
        soup = BeautifulSoup(res.text, 'lxml')

        data = soup.select('div.goodsdiv')

        flexMessage_json = '''{
                            "type": "carousel",
                            "contents": ['''
        for d in data:
            img = d.findAll('img')
            img = img[1]['src']
            a = d.findAll('a')[-1].text
            font = d.find('font')
            price = 'N' + d.text.replace(' ','').split('\xa0')[0].split('N')[1]
            f = font.text.replace('\xa0','')
            flex = '''{
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "'''+img+'''",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "action": {
                        "type": "uri",
                        "uri": "http://linecorp.com/"
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "'''+a+'''",
                            "weight": "bold",
                            "size": "md",
                            "style": "italic"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "價格:",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "'''+price+'''",
                                    "wrap": true,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "來源:",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "'''+f+'''",
                                    "wrap": true,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                                ]
                            }
                            ]
                        }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "button",
                            "style": "link",
                            "height": "sm",
                            "action": {
                            "type": "uri",
                            "label": "查看商品",
                            "uri": "'''+f"https://www.findprice.com.tw/{d.findAll('a')[-1]['href']}"+'''"
                            }
                        }
                        ],
                        "flex": 0
                    }
                    },'''
            flexMessage_json += flex
        flexMessage_json = flexMessage_json[:-1]
        flexMessage_json += ']}'
        FlexMessage = json.loads(flexMessage_json)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('熱門搜尋',FlexMessage))
    else: line_bot_api.reply_message(event.reply_token, TextSendMessage(text="目前還未開放指令查詢!"))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
