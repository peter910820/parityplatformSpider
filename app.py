from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os

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
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="目前還未開放指令查詢!"))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
