from typing import Protocol
from montag.domain import Playlist, Track


class MusicRepository(Protocol):
    def find_playlists(self) -> list[Playlist]:
        """Returns all the user's playlists."""
        ...

    def find_tracks(self, playlist_id: str) -> list[Track]:
        """Returns all tracks in the specified playlist."""
        ...
