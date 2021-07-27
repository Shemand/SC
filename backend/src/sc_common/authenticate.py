import jwt

SECRET_KEY = "isASeCreatkEy#00"

def generate_token(user_id):
    try:
        return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")
    except Exception:
        return None

def read_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None
