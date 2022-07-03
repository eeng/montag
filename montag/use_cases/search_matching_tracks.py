from dataclasses import dataclass
from typing import Optional

from montag.domain.entities import PlaylistId, Provider, TrackSuggestions
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import Response, Success, UseCase, error_handling
from pydantic import BaseModel


@dataclass
class SearchMatchingTracks(UseCase):
    repos: dict[Provider, MusicRepo]

    # TODO validate that src <> dst
    class Request(BaseModel):
        src_provider: Provider
        src_playlist_id: PlaylistId
        dst_provider: Provider
        dst_playlist_id: PlaylistId
        max_suggestions: int = 5
        limit: Optional[int] = None

    @error_handling
    def execute(self, request: Request) -> Response[list[TrackSuggestions]]:
        src_repo = self.repos[request.src_provider]
        dst_repo = self.repos[request.dst_provider]

        existing_tracks = dst_repo.find_tracks(request.dst_playlist_id)

        def calculate_suggestions(src_track):
            suggestions = dst_repo.search_matching_tracks(src_track, limit=request.max_suggestions)
            return TrackSuggestions.build(src_track, suggestions, existing_tracks)

        src_tracks = src_repo.find_tracks(request.src_playlist_id)
        track_suggestions = list(map(calculate_suggestions, src_tracks[: request.limit]))
        return Success(track_suggestions)
