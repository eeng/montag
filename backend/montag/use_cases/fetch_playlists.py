from dataclasses import dataclass

from montag.domain.entities import Playlist, Provider
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import error_handling
from montag.use_cases.types import Response, Success, UseCase


@dataclass
class FetchPlaylists(UseCase):
    repos: dict[Provider, MusicRepo]

    @error_handling
    def execute(self, provider: Provider) -> Response[list[Playlist]]:
        playlists = self.repos[provider].find_playlists()
        return Success(playlists)
