import hashlib
import hmac
import time
from flask import redirect, request
from config import BOT_TOKEN

def check_auth(data: dict) -> bool:
    auth_data = dict(data)
    hash_check = auth_data.pop('hash')
    sorted_data = "\n".join([f"{k}={auth_data[k]}" for k in sorted(auth_data)])
    secret = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_str = hmac.new(secret, sorted_data.encode(), hashlib.sha256).hexdigest()
    return hmac_str == hash_check

def telegram_user():
    return request.args.get('id')
