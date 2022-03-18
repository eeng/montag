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

    def search_tracks_matching(self, other: Track) -> list[Track]:
        response = self.client.search(other.name, filter="songs", ignore_spelling=True)
        return self._track_from_json(response)

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
