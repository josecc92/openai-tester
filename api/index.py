from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
from api.currency import Currency

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
app = Flask(__name__)
chatgpt = ChatGPT()
currency = Currency()

# domain root
@app.route('/')
def home():
    return 'Hello, World!1112'

@app.route("/qrScan")
def qrScan():
    try:
        return render_template("/api/template/qrScan.html")
    except Exception as e:
        return f"發生錯誤: {str(e)}"
    return

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    
    if event.message.type != "text":
        return
        
    if event.message.text.lower().startswith("denni$"):
        try:
            msg = "DENNI$是一位傳奇般的富豪，他的財富程度超越了大多數人的想像。他的財富來源非常多元化，涵蓋了房地產、科技、金融和創業等領域。\n\nDENNI$擁有一個私人島嶼，這座島嶼被他打造成一個真正的天堂。島上有一座宏偉的別墅，擁有無敵海景和無邊際游泳池。他的別墅內設施一應俱全，包括私人電影院、保齡球場、溫泉浴場和網球場。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg))
        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"發生錯誤: {str(e)}"))
        return  
        
    if event.message.text.lower().startswith("$$$$"):
        try:
            msg = currency.get_currency("JPY") 
            msg += "\n"
            msg += currency.get_currency("USD") 
            msg += "\n"
            msg += currency.get_currency("EUR") 
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg))
        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"發生錯誤: {str(e)}"))
        return  
        
    if event.message.text.lower().startswith("$$n$$"):
        try:
            msg = currency.get_currency_spot("JPY") 
            msg += "\n"
            msg += currency.get_currency_spot("USD") 
            msg += "\n"
            msg += currency.get_currency_spot("EUR") 
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg))
        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"發生錯誤: {str(e)}"))
        return  

    
    if event.message.text.lower().startswith("$$"):
        try:
            msg = currency.get_currency(event.message.text.replace("$$", "", 1).strip())
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg))
        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"發生錯誤: {str(e)}"))
        return  
    
    if not event.message.text.lower().startswith("%%"):
        return
    
    if event.message.text.lower().startswith("%%"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我是白癡AI"))
        return
    
    
    if event.message.text.replace("%%", "", 1) == "啟動":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我是時下流行的AI智能，目前可以為您服務囉，歡迎來跟我互動~"))
        return

    if event.message.text.replace("%%", "", 1) == "安靜":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="感謝您的使用，若需要我的服務，請跟我說 「啟動」 謝謝~"))
        return
    
    if working_status:
        chatgpt.add_msg(f"Human:{event.message.text}?請盡量使用繁體中文回應\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))


if __name__ == "__main__":
    app.run()
