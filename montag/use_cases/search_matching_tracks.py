from dataclasses import dataclass
from typing import Optional

from montag.domain.entities import (
    Playlist,
    PlaylistId,
    Provider,
    Track,
    TrackSuggestions,
)
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.decorators import error_handling
from montag.domain.errors import NotFoundError
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

        dst_playlist = fetch_mirror_playlist(
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


def fetch_mirror_playlist(
    src_playlist_id: PlaylistId, src_repo: MusicRepo, dst_repo: MusicRepo
) -> Optional[Playlist]:
    src_playlist = src_repo.find_playlist_by_id(src_playlist_id)
    if src_playlist:
        return dst_repo.find_mirror_playlist(src_playlist)
    else:
        raise NotFoundError(f"Could not find a playlist with ID '{src_playlist_id}'.")


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
