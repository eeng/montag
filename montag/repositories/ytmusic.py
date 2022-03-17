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
        return [
            Track(
                id=item["videoId"],
                name=item["title"],
                album=(item.get("album") and item["album"]["name"]),
                artists=[artist["name"] for artist in item["artists"]],
            )
            for item in response["tracks"]
        ]
