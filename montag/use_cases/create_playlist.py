from dataclasses import dataclass

from montag.domain.entities import Playlist, Provider
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import Response, Success, UseCase, error_handling
from pydantic import BaseModel


@dataclass
class CreatePlaylist(UseCase):
    repos: dict[Provider, MusicRepo]

    class Request(BaseModel):
        provider: Provider
        playlist_name: str

    @error_handling
    def execute(self, request: Request) -> Response[Playlist]:
        repo = self.repos[request.provider]
        playlist = repo.create_playlist(request.playlist_name)
        return Success(playlist)
