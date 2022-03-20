from typing import Optional, Protocol
from montag.domain import Playlist, PlaylistId, Track
from montag.util.collections import find_by


class MusicRepository(Protocol):
    def find_playlists(self) -> list[Playlist]:
        """Returns all the user's playlists."""
        ...

    def find_playlist_by_id(self, playlist_id: PlaylistId) -> Optional[Playlist]:
        return find_by(lambda p: p.id == playlist_id, self.find_playlists())

    def find_tracks(self, playlist_id: PlaylistId) -> list[Track]:
        """Returns all tracks in the specified playlist."""
        ...

    def search_matching_tracks(self, other: Track, limit=10) -> list[Track]:
        """Searches for tracks that match the one specified as best as possible."""
        ...
