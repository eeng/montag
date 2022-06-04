import functools
from dataclasses import dataclass
from typing import Generic, Optional, Protocol, TypeVar, Union

T = TypeVar("T")


@dataclass
class Success(Generic[T]):
    value: T


@dataclass
class Failure:
    msg: str
    exception: Optional[Exception] = None


Response = Union[Success[T], Failure]


class UseCase(Protocol):
    def execute(self, request: object) -> Response:
        ...

    def __call__(self, request: object) -> Response:
        return self.execute(request)


def error_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Failure(str(e) or type(e).__name__, e)

    return wrapper
