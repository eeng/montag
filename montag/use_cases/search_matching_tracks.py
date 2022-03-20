from dataclasses import dataclass
from typing import Optional
from montag.domain import (
    Playlist,
    PlaylistId,
    Provider,
    Track,
    TrackSuggestions,
)
from montag.repositories import MusicRepository
from pydantic import BaseModel

from montag.use_cases.types import Response, Ok
from montag.util.collections import find_by


class SearchMatchingTracksRequest(BaseModel):
    src_playlist_id: PlaylistId
    src_provider: Provider
    dst_provider: Provider
    max_suggestions: int = 5


class NotFoundError(Exception):
    """Raised when an entity does not exists."""


@dataclass
class SearchMatchingTracks:
    repos: dict[Provider, MusicRepository]

    def run(
        self, request: SearchMatchingTracksRequest
    ) -> Response[list[TrackSuggestions]]:
        src_repo = self.repos[request.src_provider]
        dst_repo = self.repos[request.dst_provider]

        existing_tracks = _find_existing_tracks_in_dst_playlist(
            request.src_playlist_id, src_repo, dst_repo
        )

        tracks_with_suggestions = [
            _build_track_suggestions_for(
                src_track, dst_repo, existing_tracks, request.max_suggestions
            )
            for src_track in src_repo.find_tracks(request.src_playlist_id)
        ]
        return Ok(tracks_with_suggestions)


def _find_existing_tracks_in_dst_playlist(
    src_playlist_id: PlaylistId, src_repo: MusicRepository, dst_repo: MusicRepository
):
    src_playlist = src_repo.find_playlist_by_id(src_playlist_id)
    if not src_playlist:
        raise NotFoundError(src_playlist_id)
    dst_playlist = find_corresponding_playlist(src_playlist, dst_repo.find_playlists())
    return dst_repo.find_tracks(dst_playlist.id) if dst_playlist else []


def find_corresponding_playlist(
    src_playlist: Playlist, dst_playlists: list[Playlist]
) -> Optional[Playlist]:
    def is_liked_or_has_same_name(p: Playlist):
        return p.is_liked if src_playlist.is_liked else src_playlist.name == p.name

    return find_by(is_liked_or_has_same_name, dst_playlists)


def _build_track_suggestions_for(
    src_track: Track,
    dst_repo: MusicRepository,
    existing_tracks: list[Track],
    max_suggestions: int,
):
    suggestions = dst_repo.search_matching_tracks(src_track, limit=max_suggestions)
    already_present = [s.id for s in suggestions if s in existing_tracks]
    return TrackSuggestions(
        target=src_track, suggestions=suggestions, already_present=already_present
    )
