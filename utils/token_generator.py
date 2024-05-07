import time
from os import environ as env

import jwt

secret = env["TOKEN_SECRET"]
algorithm = "HS256"


def generate_auth_token(user):
    auth_token = jwt.encode(
        payload={
            "user_id": user.user_id,
            "email": user.email,
            "token_expiry": int(time.time()) + int(env['TOKEN_EXPIRY_BY'])
        },
        key=secret,
        algorithm=algorithm
    )

    return auth_token


def __user_model(auth_token):
    user_model = jwt.decode(auth_token, secret, algorithm)
    return user_model


def valid_token(auth_token):
    user = __user_model(auth_token)
    time_now = int(time.time())
    if user['token_expiry'] >= time_now:
        return True
    return False

