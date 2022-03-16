from typing import Protocol
from montag.domain import Playlist


class MusicRepository(Protocol):
    def find_playlists(self) -> list[Playlist]:
        ...
