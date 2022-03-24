from typing import Optional, Protocol
from montag.domain.entities import Playlist, PlaylistId, Track
from montag.util.collections import find_by


class MusicRepo(Protocol):
    def find_playlists(self) -> list[Playlist]:
        """Returns all the user's playlists."""
        ...

    def find_tracks(self, playlist_id: PlaylistId) -> list[Track]:
        """Returns all tracks in the specified playlist."""
        ...

    def search_matching_tracks(self, target: Track, limit=10) -> list[Track]:
        """Searches for tracks that match the one specified as best as possible."""
        ...

    def create_playlist(self, name: str) -> PlaylistId:
        """Creates a new playlist for the current user, and returns its ID"""
        ...

    def find_playlist_by_id(self, playlist_id: PlaylistId) -> Optional[Playlist]:
        return find_by(lambda p: p.id == playlist_id, self.find_playlists())

    def find_mirror_playlist(self, other: Playlist) -> Optional[Playlist]:
        def is_liked_or_has_same_name(p: Playlist):
            return p.is_liked if other.is_liked else other.name == p.name

        return find_by(is_liked_or_has_same_name, self.find_playlists())
