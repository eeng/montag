from dataclasses import dataclass
from typing import Optional, Protocol
from montag.models import Playlist, Track
from montag.repositories import MusicRepository


class SpotifyClient(Protocol):
    def my_playlists(self) -> dict:
        ...

    def liked_tracks(self, limit: int, offset: int = 0) -> dict:
        ...

    def playlist_tracks(self, playlist_id: str, limit: int, offset: int = 0) -> dict:
        ...


@dataclass
class SpotifyRepo(MusicRepository):
    client: SpotifyClient

    def find_playlists(self):
        response = self.client.my_playlists()
        return [
            Playlist(id=item["id"], name=item["name"]) for item in response["items"]
        ]

    def find_tracks(self, playlist_id: Optional[str] = None) -> list[Track]:
        """Returns all tracks in the specified playlist, or if None provided, gets the user's liked songs."""
        total = self._fetch_liked_or_playlist_tracks(playlist_id, limit=1)["total"]
        limit = 50
        return [
            track
            for offset in range(0, total + 1, limit)
            for track in self.find_tracks_batch(playlist_id, limit=limit, offset=offset)
        ]

    def find_tracks_batch(self, playlist_id=None, **kargs) -> list[Track]:
        response = self._fetch_liked_or_playlist_tracks(playlist_id, **kargs)
        return [
            Track(
                name=item["track"]["name"],
                uri=item["track"]["uri"],
                album=item["track"]["album"]["name"],
                artists=[artist["name"] for artist in item["track"]["artists"]],
            )
            for item in response["items"]
        ]

    def _fetch_liked_or_playlist_tracks(self, playlist_id=None, **kwargs):
        if playlist_id:
            return self.client.playlist_tracks(playlist_id, **kwargs)
        else:
            return self.client.liked_tracks(**kwargs)
