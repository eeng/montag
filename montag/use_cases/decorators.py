import functools
import logging
from montag.domain.errors import ApplicationError

from montag.use_cases.types import Failure


def error_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApplicationError as e:
            return Failure(str(e))
        except Exception as e:
            logging.exception(e)
            return Failure(str(e))

    return wrapper
