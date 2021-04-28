from flask import g
from functools import wraps

# ----- COMMON FUNCTIONS -----



# ----- DECORATORS -----


def required_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.response.loggined:
            return func(*args, **kwargs)
        return g.response.unauth().get()
    return decorated_function
