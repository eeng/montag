import functools

from montag.use_cases.types import Failure


def error_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Failure(str(e) or type(e).__name__, e)

    return wrapper
