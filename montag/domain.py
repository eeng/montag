from enum import Enum
from typing import Optional

from pydantic import BaseModel

TrackId = str
PlaylistId = str


class Track(BaseModel):
    id: TrackId
    name: str
    album: Optional[str]
    artists: list[str]


class Playlist(BaseModel):
    id: PlaylistId
    name: str


class Provider(Enum):
    SPOTIFY = "Spotify"
    YT_MUSIC = "YouTubeMusic"
