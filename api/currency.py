from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
from api.currency import Currency
from api.ASACalculator import ASACalculator

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
app = Flask(__name__)
chatgpt = ChatGPT()
currency = Currency()

def is_float(value):
    try:
        float_value = float(value)
        return True
    except ValueError:
        return False
    
# domain root
@app.route('/')
def home():
    return 'Hello, World!0613'

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
         
    try:
        if event.message.text.lower().startswith("version"):
            msg = "20240613"
            
        elif event.message.text.lower().startswith("denni$"):
            msg = "你問的好，DENNI$是一位傳奇般的富豪，他的財富程度超越了大多數人的想像。他的財富來源非常多元化，涵蓋了房地產、科技、金融和創業等領域。\n\nDENNI$擁有一個私人島嶼，這座島嶼被他打造成一個真正的天堂。島上有一座宏偉的別墅，擁有無敵海景和無邊際游泳池。他的別墅內設施一應俱全，包括私人電影院、保齡球場、溫泉浴場和網球場。"

        elif event.message.text.lower().startswith("asmiles"):
            user_message = event.message.text.strip().lower()
            # 切分訊息為單詞列表
            words = user_message.split()
            
            if (len(words) == 4 and words[0] == "asmiles" and is_float(words[1]) and is_float(words[2]))or (len(words) == 5 and words[0] == "asmiles" and is_float(words[1]) and is_float(words[2]) and is_float(words[4])):
                if words[3].lower().strip() == "cash":
                    ASACalculator.get_asa_mile_unit_price(words[2], float(words[1]), "本行現金賣出")
                elif words[3].lower().strip() == "spot":
                    ASACalculator.get_asa_mile_unit_price(words[2], float(words[1]), "本行即期賣出")
                else:
                    msg = "指令不正確，使用以下格式\nasmiles <購買里程數> <獲得的里程百分比> <cash 或 spot> <來回機票所用里程:非必要>"
            else:
                msg = "指令不正確，使用以下格式\nasmiles <購買里程數> <獲得的里程百分比> <cash 或 spot> <來回機票所用里程:非必要>"
            # 將 words 列表的內容顯示為字串
            words_str = ' '.join(words)
            msg += f"\n切分後的訊息：{words_str}"
            msg += f"{len(words)} and {words[0]} and {words[1]} and {words[2]}"
            msg += f"{len(words)} and {words[0]} and {words[1]} and {words[2]} and {words[4]}"
            
        # currency
        elif event.message.text.lower().startswith("$$$$"):
            msg = currency.get_currency("JPY") 
            msg += "\n"
            msg += currency.get_currency("USD") 
            msg += "\n"
            msg += currency.get_currency("EUR") 
        
        elif event.message.text.lower().startswith("$$n$$"):
            msg = currency.get_currency_spot("JPY") 
            msg += "\n"
            msg += currency.get_currency_spot("USD") 
            msg += "\n"
            msg += currency.get_currency_spot("EUR") 

        
        elif event.message.text.lower().startswith("$$"):
            msg = currency.get_currency(event.message.text.replace("$$", "", 1).strip())

    except Exception as e:
        msg = f"發生錯誤: {str(e)}"

    finally:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )    
    
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
