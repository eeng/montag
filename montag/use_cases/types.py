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
