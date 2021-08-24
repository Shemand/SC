from flask import g
from functools import wraps

# ----- COMMON FUNCTIONS -----



# ----- DECORATORS -----


def required_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.middleware.loggined:
            return func(*args, **kwargs)
        return g.middleware.unauth().get()
    return decorated_function
