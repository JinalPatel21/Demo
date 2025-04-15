import jwt
import time
import os


API_KEY = os.getenv("VIDEOSDK_API_KEY")
SECRET = os.getenv("VIDEOSDK_SECRET")


def generate_videosdk_token():
    payload = {
        "apikey": API_KEY,
        "permissions": ["allow_join", "allow_mod"],
        "iat": int(time.time()),
        "exp": int(time.time()) + 24 * 3600
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token
