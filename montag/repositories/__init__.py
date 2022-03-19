from typing import Protocol
from montag.domain import Playlist, PlaylistId, Track


class MusicRepository(Protocol):
    def find_playlists(self) -> list[Playlist]:
        """Returns all the user's playlists."""
        ...

    def find_tracks(self, playlist_id: PlaylistId) -> list[Track]:
        """Returns all tracks in the specified playlist."""
        ...

    def search_matching_tracks(self, other: Track, limit=10) -> list[Track]:
        """Searches for tracks that match the one specified as best as possible."""
        ...
