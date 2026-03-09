import requests
import os


def main():
    TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
    USER_ID = os.getenv("LINE_USER_ID")
    url = "https://api.line.me/v2/bot/message/push"

    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": "Python job finished"}],
    }

    res = requests.post(url, headers=headers, json=data)

    print(res.status_code)
    print(res.text)


if __name__ == "__main__":
    main()
