from dataclasses import dataclass

from montag.domain.entities import PlaylistId, Provider, Track, TrackSuggestions
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.support import error_handling, fetch_mirror_playlist
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

        _, dst_playlist = fetch_mirror_playlist(
            request.src_playlist_id, src_repo, dst_repo
        )
        existing_tracks = dst_repo.find_tracks(dst_playlist.id) if dst_playlist else []

        tracks_with_suggestions = [
            _search_suggestions_for(
                src_track, dst_repo, existing_tracks, request.max_suggestions
            )
            for src_track in src_repo.find_tracks(request.src_playlist_id)
        ]
        return Success(tracks_with_suggestions)


# TODO move this to the domain?
def _search_suggestions_for(
    src_track: Track,
    dst_repo: MusicRepo,
    existing_tracks: list[Track],
    max_suggestions: int,
):
    suggestions = dst_repo.search_matching_tracks(src_track, limit=max_suggestions)
    already_present = [s.id for s in suggestions if s in existing_tracks]
    return TrackSuggestions(
        target=src_track, suggestions=suggestions, already_present=already_present
    )
