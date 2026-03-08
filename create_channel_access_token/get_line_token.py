import jwt
import json
import time
import requests
from jwt.algorithms import RSAAlgorithm

# ===== 設定 =====
CHANNEL_ID = "2009361640"
KID = "f1010156-f490-4cec-a723-30cd17782032"  # KID = Assertion Signing Key

with open("./private.key", "r") as f:
    private_key = json.load(f)
print(private_key)


# ===== JWT header =====
headers = {"alg": "RS256", "typ": "JWT", "kid": KID}

# ===== JWT payload =====
payload = {
    "iss": CHANNEL_ID,
    "sub": CHANNEL_ID,
    "aud": "https://api.line.me/",
    "exp": int(time.time()) + 1800,
    "token_exp": 60 * 60 * 24 * 30,
}

# ===== JWT生成 =====
key = RSAAlgorithm.from_jwk(json.dumps(private_key))

jwt_token = jwt.encode(payload, key, algorithm="RS256", headers=headers)

print("JWT created")

# ===== LINE API =====
url = "https://api.line.me/oauth2/v2.1/token"

data = {
    "grant_type": "client_credentials",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": jwt_token,
}

res = requests.post(url, data=data)

print("Status:", res.status_code)
print("Response:")
print(res.text)
