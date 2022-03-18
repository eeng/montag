from typing import Protocol
from montag.domain import Playlist, Track


class MusicRepository(Protocol):
    def find_playlists(self) -> list[Playlist]:
        """Returns all the user's playlists."""
        ...

    def find_tracks(self, playlist_id: str) -> list[Track]:
        """Returns all tracks in the specified playlist."""
        ...

    def search_tracks_matching(self, other: Track) -> list[Track]:
        """Searches for tracks that match the other as best as possible."""
        ...
