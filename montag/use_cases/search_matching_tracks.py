from dataclasses import dataclass

from montag.domain.entities import PlaylistId, Provider, TrackSuggestions
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import error_handling
from montag.use_cases.types import Response, Success, UseCase
from pydantic import BaseModel


@dataclass
class SearchMatchingTracks(UseCase):
    repos: dict[Provider, MusicRepo]

    class Request(BaseModel):
        src_provider: Provider
        dst_provider: Provider
        src_playlist_id: PlaylistId
        max_suggestions: int = 5

    @error_handling
    def execute(self, request: Request) -> Response[list[TrackSuggestions]]:
        src_repo = self.repos[request.src_provider]
        dst_repo = self.repos[request.dst_provider]

        src_playlist = src_repo.get_playlist_by_id(request.src_playlist_id)
        dst_playlist = dst_repo.find_mirror_playlist(src_playlist)
        existing_tracks = dst_repo.find_tracks(dst_playlist.id) if dst_playlist else []

        def calculate_suggestions(src_track):
            suggestions = dst_repo.search_matching_tracks(src_track, limit=request.max_suggestions)
            return TrackSuggestions.build(src_track, suggestions, existing_tracks)

        track_suggestions = list(
            map(calculate_suggestions, src_repo.find_tracks(request.src_playlist_id))
        )
        return Success(track_suggestions)
