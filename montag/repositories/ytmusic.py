from dataclasses import dataclass
from ytmusicapi import YTMusic
from montag.domain import Playlist, Track
from montag.repositories import MusicRepository


@dataclass
class YouTubeMusicRepo(MusicRepository):
    client: YTMusic

    def find_playlists(self) -> list[Playlist]:
        response = self.client.get_library_playlists()
        return [
            Playlist(id=item["playlistId"], name=item["title"]) for item in response
        ]

    def find_tracks(self, playlist_id: str) -> list[Track]:
        response = self.client.get_playlist(playlistId=playlist_id)
        return self._track_from_json(response["tracks"])

    def search_tracks_matching(self, other: Track, limit=10) -> list[Track]:
        q = f"{other.name} {other.artists[0]}"
        response = self.client.search(q, filter="songs", limit=limit)
        # Slicing here since YTMusic seems to ignore the limit param
        return self._track_from_json(response[0:limit])

    def _track_from_json(self, tracks_json: list[dict]):
        return [
            Track(
                id=item["videoId"],
                name=item["title"],
                album=(item.get("album") and item["album"]["name"]),
                artists=[artist["name"] for artist in item["artists"]],
            )
            for item in tracks_json
        ]
