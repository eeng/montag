from dataclasses import dataclass

from montag.domain import PlaylistId, Provider, Track, TrackSuggestions
from montag.repositories.music_repo import MusicRepo
from montag.use_cases import error_handling
from montag.use_cases.errors import NotFoundError
from montag.use_cases.types import Response, Success, UseCase
from pydantic import BaseModel


class SearchMatchingTracksRequest(BaseModel):
    src_playlist_id: PlaylistId
    src_provider: Provider
    dst_provider: Provider
    max_suggestions: int = 5


@dataclass
class SearchMatchingTracks(UseCase):
    repos: dict[Provider, MusicRepo]

    @error_handling
    def execute(
        self, request: SearchMatchingTracksRequest
    ) -> Response[list[TrackSuggestions]]:
        src_repo = self.repos[request.src_provider]
        dst_repo = self.repos[request.dst_provider]

        existing_tracks = _find_existing_tracks_in_dst_playlist(
            request.src_playlist_id, src_repo, dst_repo
        )

        tracks_with_suggestions = [
            _search_suggestions_for(
                src_track, dst_repo, existing_tracks, request.max_suggestions
            )
            for src_track in src_repo.find_tracks(request.src_playlist_id)
        ]
        return Success(tracks_with_suggestions)


def _find_existing_tracks_in_dst_playlist(
    src_playlist_id: PlaylistId, src_repo: MusicRepo, dst_repo: MusicRepo
):
    src_playlist = src_repo.find_playlist_by_id(src_playlist_id)
    if not src_playlist:
        raise NotFoundError(f"Could not find a playlist with ID '{src_playlist_id}'.")

    dst_playlist = dst_repo.find_mirror_playlist(src_playlist)

    return dst_repo.find_tracks(dst_playlist.id) if dst_playlist else []


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
