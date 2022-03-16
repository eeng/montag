from dataclasses import dataclass
from ytmusicapi import YTMusic
from montag.domain import Playlist
from montag.repositories import MusicRepository


@dataclass
class YouTubeMusicRepo(MusicRepository):
    client: YTMusic

    def find_playlists(self) -> list[Playlist]:
        response = self.client.get_library_playlists()
        return [
            Playlist(id=item["playlistId"], name=item["title"]) for item in response
        ]
