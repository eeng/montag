from dataclasses import dataclass

from montag.clients.spotify import SpotifyClient
from montag.domain import Playlist, PlaylistId, Track
from montag.repositories import MusicRepository

LIKED_SONGS_ID = "LS"


@dataclass
class SpotifyRepo(MusicRepository):
    client: SpotifyClient

    def find_playlists(self) -> list[Playlist]:
        response = self.client.my_playlists()
        other_playlists = [
            Playlist(id=item["id"], name=item["name"]) for item in response["items"]
        ]
        liked_songs_playlist = Playlist(id=LIKED_SONGS_ID, name="Liked Songs")
        return [liked_songs_playlist, *other_playlists]

    def find_tracks(self, playlist_id: PlaylistId) -> list[Track]:
        """Returns all tracks in the specified playlist. Use playlist_id='LS' to get the liked songs"""
        total = self._fetch_liked_or_playlist_tracks(playlist_id, limit=1)["total"]
        limit = 50
        return [
            track
            for offset in range(0, total + 1, limit)
            for track in self._find_tracks_batch(
                playlist_id=playlist_id, limit=limit, offset=offset
            )
        ]

    def _find_tracks_batch(self, **kargs) -> list[Track]:
        response = self._fetch_liked_or_playlist_tracks(**kargs)
        return [
            Track(
                id=item["track"]["id"],
                name=item["track"]["name"],
                album=item["track"]["album"]["name"],
                artists=[artist["name"] for artist in item["track"]["artists"]],
            )
            for item in response["items"]
        ]

    def _fetch_liked_or_playlist_tracks(self, playlist_id, **kwargs):
        if playlist_id == LIKED_SONGS_ID:
            return self.client.liked_tracks(**kwargs)
        else:
            return self.client.playlist_tracks(playlist_id, **kwargs)

    def search_matching_tracks(self, other: Track, limit=10) -> list[Track]:
        q = f"track:{other.name} artist:{other.artists[0]}"
        response = self.client.search(q, type="track", limit=limit)
        return [
            Track(
                id=item["id"],
                name=item["name"],
                album=item["album"]["name"],
                artists=[artist["name"] for artist in item["artists"]],
            )
            for item in response["tracks"]["items"]
        ]
