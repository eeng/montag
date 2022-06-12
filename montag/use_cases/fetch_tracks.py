from dataclasses import dataclass

from montag.domain.entities import PlaylistId, Provider, Track
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import Response, Success, UseCase, error_handling
from pydantic import BaseModel


@dataclass
class FetchTracks(UseCase):
    repos: dict[Provider, MusicRepo]

    class Request(BaseModel):
        provider: Provider
        playlist_id: PlaylistId

    @error_handling
    def execute(self, request: Request) -> Response[list[Track]]:
        tracks = self.repos[request.provider].find_tracks(request.playlist_id)
        return Success(tracks)
