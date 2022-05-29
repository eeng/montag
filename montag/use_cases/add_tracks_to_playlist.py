from dataclasses import dataclass

from montag.domain.entities import PlaylistId, Provider, TrackId
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import error_handling
from montag.use_cases.types import Response, Success, UseCase
from pydantic import BaseModel


@dataclass
class AddTracksToPlaylist(UseCase):
    repos: dict[Provider, MusicRepo]

    class Request(BaseModel):
        provider: Provider
        playlist_id: PlaylistId
        track_ids: list[TrackId]

    @error_handling
    def execute(self, request: Request) -> Response[None]:
        repo = self.repos[request.provider]
        repo.add_tracks(request.playlist_id, request.track_ids)
        return Success(None)
