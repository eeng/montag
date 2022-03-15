from dataclasses import dataclass
from typing import Protocol
from montag.models import Playlist
from montag.repositories import MusicRepository


class YouTubeMusicClient(Protocol):
    def my_playlists(self) -> list[dict]:
        ...


@dataclass
class YouTubeMusicRepo(MusicRepository):
    client: YouTubeMusicClient

    def find_playlists(self):
        response = self.client.my_playlists()
        return [
            Playlist(id=item["playlistId"], name=item["title"]) for item in response
        ]
