from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar, Union


T = TypeVar("T")


@dataclass
class Success(Generic[T]):
    value: T


@dataclass
class Failure:
    msg: str

    @property
    def value(self):
        return {"error": self.msg}


Response = Union[Success[T], Failure]


class UseCase(Protocol):
    def execute(self, request: object) -> Response:
        ...
