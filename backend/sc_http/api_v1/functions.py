from functools import wraps

# ----- COMMON FUNCTIONS -----



# ----- DECORATORS -----
def required_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.loggined:
            return True
        return False
    return decorated_function