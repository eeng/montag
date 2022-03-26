from dataclasses import dataclass

from montag.domain.entities import Playlist, PlaylistId, Provider, TrackId
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import error_handling, fetch_mirror_playlist
from montag.use_cases.types import Response, Success, UseCase
from pydantic import BaseModel


@dataclass
class AddTracksToMirrorPlaylist(UseCase):
    repos: dict[Provider, MusicRepo]

    class Request(BaseModel):
        src_provider: Provider
        dst_provider: Provider
        src_playlist_id: PlaylistId
        dst_track_ids: list[TrackId]

    @error_handling
    def execute(self, request: Request) -> Response[Playlist]:
        src_repo = self.repos[request.src_provider]
        dst_repo = self.repos[request.dst_provider]

        src_playlist, dst_playlist = fetch_mirror_playlist(request.src_playlist_id, src_repo, dst_repo)
        if not dst_playlist:
            dst_playlist = dst_repo.create_playlist(src_playlist.name)

        dst_repo.add_tracks(dst_playlist.id, request.dst_track_ids)

        return Success(dst_playlist)
