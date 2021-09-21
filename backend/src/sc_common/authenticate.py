import os

import jwt
import os


def generate_token(user_name):
    try:
        return jwt.encode({"user_name": user_name}, os.environ.get('JWT_SECRET_KEY'), algorithm="HS256")
    except Exception:
        return None

def read_token(token):
    try:
        return jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=["HS256"])
    except Exception:
        return None
