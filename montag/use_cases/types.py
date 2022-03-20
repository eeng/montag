from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar, Union


T = TypeVar("T")


@dataclass
class Success(Generic[T]):
    value: T


@dataclass
class Failure:
    type: str
    msg: str

    @property
    def value(self):
        return {"type": self.type, "msg": self.msg}


Response = Union[Success[T], Failure]


class UseCase(Protocol):
    def execute(self, request: object) -> Response:
        ...
