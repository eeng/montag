from dataclasses import dataclass
from typing import Optional
from montag.gateways.spotify import SpotifyClient
from montag.models import Track


@dataclass
class SpotifyRepo:
    client: SpotifyClient

    def find_all_tracks(self, playlist_id: Optional[str] = None) -> list[Track]:
        """Returns all tracks in the specified playlist, or if None provided, gets the user's liked songs."""
        total = self._fetch_liked_or_playlist_tracks(playlist_id, limit=1)["total"]
        limit = 50
        return [
            track
            for offset in range(0, total + 1, limit)
            for track in self.find_tracks(playlist_id, limit=limit, offset=offset)
        ]

    def find_tracks(self, playlist_id=None, **kargs) -> list[Track]:
        tracks_json = self._fetch_liked_or_playlist_tracks(playlist_id, **kargs)
        return [
            Track(
                name=item["track"]["name"],
                uri=item["track"]["uri"],
                album=item["track"]["album"]["name"],
                artists=[artist["name"] for artist in item["track"]["artists"]],
            )
            for item in tracks_json["items"]
        ]

    def _fetch_liked_or_playlist_tracks(self, playlist_id=None, **kwargs):
        if playlist_id:
            return self.client.playlist_tracks(playlist_id, **kwargs)
        else:
            return self.client.my_tracks(**kwargs)
