from typing import Protocol
from montag.models import Playlist


class MusicRepository(Protocol):
    def find_playlists(self) -> list[Playlist]:
        ...
