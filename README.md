# In Remote
1. Login LINE Developers
2. Create Provider (Ex: Daichi\_Private\_Provider)
3. Create "Massaging API" channel
4. Create LINE Official Account (Ex: Deech\_official)  
   This is the channel you recieve a message.

# In Local
5. Create private and public key
6. Set public key in created channel
7. Create channel access token  
   (Ref: https://qiita.com/knaot0/items/8427918564400968bd2b )  
8. Test main.py



* Ref: https://developers.line.biz/ja/docs/messaging-api/generate-json-web-token/#generate-a-key-pair-for-the-assertion-signing-key

  ---  
import os
import threading
import subprocess
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
CHANNEL_TOKEN = os.environ["LINE_CHANNEL_TOKEN"]

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

def run_job(user_id, command):
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    line_bot_api.push_message(user_id, TextSendMessage(text=f"ジョブ完了: {output}"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        events = parser.parse(body, signature)
    except Exception:
        abort(400)

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            text = event.message.text.strip()
            user_id = event.source.user_id
            if text.startswith("run job"):
                job_name = text.split()[2]
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"{job_name}を開始します"))
                threading.Thread(target=run_job, args=(user_id, ["python", f"{job_name}.py"]), daemon=True).start()
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="コマンド例: run job <name>"))

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
