from typing import Protocol


class MusicRepository(Protocol):
    def find_playlists(self):
        ...
