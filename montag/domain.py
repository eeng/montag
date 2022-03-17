from typing import Optional
from pydantic import BaseModel


class Track(BaseModel):
    id: str
    name: str
    album: Optional[str]
    artists: list[str]


class Playlist(BaseModel):
    id: str
    name: str
