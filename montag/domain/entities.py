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

    # YouTube Music treats the liked songs a special playlist with id=LM.
    # Spotify however, doesn't treat the Liked Songs as a playlist,
    # so I'll create one to unify the behavior and mark both of them with this flag.
    is_liked: bool = False


class TrackSuggestions(BaseModel):
    # Track found in source playlist
    target: Track

    # List of tracks matching the target suggested by the dst provider
    suggestions: list[Track]

    # TrackIds of suggestions that already exist in the destination playlist
    already_present: list[TrackId] = []


class Provider(Enum):
    SPOTIFY = "Spotify"
    YT_MUSIC = "YouTubeMusic"