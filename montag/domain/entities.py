from enum import Enum
from typing import Optional

from pydantic import BaseModel

PlaylistId = str
TrackId = str


class Provider(Enum):
    SPOTIFY = "spotify"
    YT_MUSIC = "ytmusic"


LikedSongsPlaylistByProvider = {
    Provider.SPOTIFY: "LS",
    Provider.YT_MUSIC: "LM",
}


class Playlist(BaseModel):
    id: PlaylistId
    name: str

    # YouTube Music treats the liked songs a special playlist with id=LM.
    # Spotify however, doesn't treat the Liked Songs as a playlist,
    # so I'll create one to unify the behavior and mark both of them with this flag.
    is_liked: bool = False


class Track(BaseModel):
    id: TrackId
    name: str
    album: Optional[str]
    artists: list[str]


class SuggestedTrack(Track):
    ## Indicates whether the track already exists in the destination playlist
    already_present: bool

    @classmethod
    def build(cls, track: Track, already_present: bool = False):
        return cls(**track.dict(), already_present=already_present)


class TrackSuggestions(BaseModel):
    # Track found in source playlist
    target: Track

    # List of tracks matching the target suggested by the dst provider
    suggestions: list[SuggestedTrack]

    @classmethod
    def build(cls, src_track: Track, suggestions: list[Track], existing_tracks: list[Track]):
        suggested_tracks = [
            SuggestedTrack.build(s, already_present=(s in existing_tracks)) for s in suggestions
        ]
        return cls(target=src_track, suggestions=suggested_tracks)

    @property
    def is_some_already_present(self) -> bool:
        return any([s.already_present for s in self.suggestions])
