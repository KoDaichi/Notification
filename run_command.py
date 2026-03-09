import os
import threading
import subprocess

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# =============================
# Environment variables
# =============================

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_TOKEN:
    raise RuntimeError("LINE environment variables are not set")

# =============================
# LINE setup
# =============================

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

# =============================
# Allowed jobs (security)
# =============================

ALLOWED_JOBS = {
    "test": "test.py",
    "analysis": "analysis.py",
    "notify": "notify.py",
}

# =============================
# Job runner
# =============================


def run_job(user_id, command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=600,
        )

        output = result.stdout.strip() or result.stderr.strip()

        if not output:
            output = "ジョブ完了 (出力なし)"

    except subprocess.TimeoutExpired:
        output = "ジョブがタイムアウトしました"

    except Exception as e:
        output = f"エラー: {str(e)}"

    line_bot_api.push_message(user_id, TextSendMessage(text=f"結果:\n{output[:4000]}"))


# =============================
# System commands
# =============================


def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return str(e)


# =============================
# Webhook endpoint
# =============================


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except Exception:
        abort(400)

    for event in events:
        if not isinstance(event, MessageEvent):
            continue

        if not isinstance(event.message, TextMessage):
            continue

        text = event.message.text.strip()
        user_id = event.source.user_id

        # -------------------------
        # Run job
        # -------------------------

        if text.startswith("run job"):
            parts = text.split()

            if len(parts) < 3:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="使い方: run job <name>")
                )
                return "OK"

            job_name = parts[2]

            if job_name not in ALLOWED_JOBS:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="そのジョブは許可されていません"),
                )
                return "OK"

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=f"{job_name} を開始します")
            )

            threading.Thread(
                target=run_job,
                args=(user_id, ["python", ALLOWED_JOBS[job_name]]),
                daemon=True,
            ).start()

        # -------------------------
        # GPU status
        # -------------------------

        elif text == "gpu":
            output = run_command(["nvidia-smi"])

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=output[:4000])
            )

        # -------------------------
        # Disk usage
        # -------------------------

        elif text == "disk":
            output = run_command(["df", "-h"])

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=output[:4000])
            )

        # -------------------------
        # Help
        # -------------------------

        else:
            help_text = """
コマンド一覧

run job <name>
gpu
disk
"""

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=help_text)
            )

    return "OK", 200


# =============================
# Start server
# =============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
