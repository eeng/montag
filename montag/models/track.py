from unittest.mock import Base
from pydantic import BaseModel


class Track(BaseModel):
    name: str
    uri: str
    album: str
    artists: list[str]
