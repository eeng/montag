from typing import Optional, Protocol
from montag.domain.entities import Playlist, PlaylistId, Track, TrackId
from montag.domain.errors import NotFoundError
from montag.util.collections import find_by


class MusicRepo(Protocol):
    def find_playlists(self) -> list[Playlist]:
        """Returns all the user's playlists."""
        ...

    # TODO make sure this throws NotFoundError when the playlist doesn't exists
    def find_tracks(self, playlist_id: PlaylistId) -> list[Track]:
        """Returns all tracks in the specified playlist."""
        ...

    def search_matching_tracks(self, target: Track, limit=10) -> list[Track]:
        """Searches for tracks that match the one specified as best as possible."""
        ...

    def create_playlist(self, name: str) -> Playlist:
        """Creates a new playlist for the current user, and returns it"""
        ...

    def add_tracks(self, playlist_id: PlaylistId, track_ids: list[TrackId]) -> None:
        """Adds the specified tracks to the playlist."""
        ...

    def find_playlist_by_id(self, playlist_id: PlaylistId) -> Optional[Playlist]:
        return find_by(lambda p: p.id == playlist_id, self.find_playlists())

    def get_playlist_by_id(self, playlist_id: PlaylistId) -> Playlist:
        if playlist := self.find_playlist_by_id(playlist_id):
            return playlist
        else:
            raise NotFoundError(f"Could not find a playlist with ID '{playlist_id}'")

    def find_mirror_playlist(self, other: Playlist) -> Optional[Playlist]:
        def is_liked_or_has_same_name(p: Playlist):
            return p.is_liked if other.is_liked else other.name == p.name

        return find_by(is_liked_or_has_same_name, self.find_playlists())
