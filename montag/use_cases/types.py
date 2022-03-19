from dataclasses import dataclass
from typing import Generic, TypeVar, Union


SuccessValue = TypeVar("SuccessValue")


@dataclass
class Ok(Generic[SuccessValue]):
    value: SuccessValue


@dataclass
class Error:
    type: str
    msg: str

    @property
    def value(self):
        return {"type": self.type, "msg": self.msg}


Response = Union[Ok[SuccessValue], Error]
