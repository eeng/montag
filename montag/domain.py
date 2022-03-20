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


class TrackSuggestions(BaseModel):
    # Track found in source playlist
    target: Track

    # List of tracks matching the target suggested by the dst provider
    suggestions: list[Track]

    # TrackIds of suggestions that are already in the user's library
    in_library: list[TrackId]
