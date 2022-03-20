from dataclasses import dataclass
from montag.domain import Playlist, Provider
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.types import Success, Response, UseCase


@dataclass
class FetchPlaylists(UseCase):
    repos: dict[Provider, MusicRepo]

    def execute(self, provider: Provider) -> Response[list[Playlist]]:
        return Success(self.repos[provider].find_playlists())
