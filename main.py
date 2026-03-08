import requests


def main():
    token = "eyJhbGciOiJIUzI1NiJ9.bbL5b8TE2_JF0l1yjD5GRKVwyD0K6BPbC4oFyoH0NfM3wIx0Vn0GCIHt0gWJv4BbzIO5Oe6NvLUQlEeSvRAtf76_eaUOk9b1PE5sHzJ0AgmaxqJU3dDmlwh_fIyMpqPC.4rbreZzOoFyNpTeoChdz-g5ikhXpEhuokSQfikSQEwA"
    user_id = "U537e5d74199a78776902ceea191dab97"

    url = "https://api.line.me/v2/bot/message/push"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": "Python job finished"}],
    }

    res = requests.post(url, headers=headers, json=data)

    print(res.status_code)
    print(res.text)


if __name__ == "__main__":
    main()
