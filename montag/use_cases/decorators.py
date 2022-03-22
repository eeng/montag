import functools

from montag.use_cases.types import Failure


def error_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # TODO log exception
            return Failure(str(e))

    return wrapper
