from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.models import (
    FlexSendMessage, 
    BubbleContainer
)
from chatgpt import ChatGPT
import os
from dotenv import load_dotenv

load_dotenv()
config = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
api_client = ApiClient(config)
line_bot_api = MessagingApi(api_client)
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFAULT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'I am Robot'

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


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    global working_status
    
    if event.message.type != "text":
        return

    working_status = True
    app.logger.info("Process "+event.message.text)    
    if working_status:
        chatgpt.add_msg(f"Human:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        reply_msg="{\"type\": \"bubble\",\"body\": {\"type\": \"box\",\"layout\": \"vertical\",\"contents\": [{\"type\": \"text\",\"text\": \"hello, world\"}])}"       
        flex_message = FlexSendMessage(alt_text="Hello Ntcu", contents=reply_msg)
        line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token,messages=[TextMessage(text="hello")]))
        #line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token,messages=[TextMessage(text=reply_msg)]))


if __name__ == "__main__":
    app.run()