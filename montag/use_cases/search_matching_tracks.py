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


class SearchMatchingTracksRequest(BaseModel):
    src_playlist_id: PlaylistId
    src_provider: Provider
    dst_provider: Provider


SearchMatchingTracksResponse = Response[list[TrackSuggestions]]


@dataclass
class SearchMatchingTracks:
    repos: dict[Provider, MusicRepository]

    def run(self, request: SearchMatchingTracksRequest) -> SearchMatchingTracksResponse:
        src_repo = self.repos[request.src_provider]
        dst_repo = self.repos[request.dst_provider]

        existing_tracks = find_existing_tracks_in_dst_playlist(
            request.src_playlist_id, src_repo, dst_repo
        )

        tracks_with_suggestions = [
            build_track_suggestions_for(src_track, dst_repo, existing_tracks)
            for src_track in src_repo.find_tracks(request.src_playlist_id)
        ]
        return Ok(tracks_with_suggestions)


def find_existing_tracks_in_dst_playlist(
    src_playlist_id: PlaylistId, src_repo: MusicRepository, dst_repo: MusicRepository
):
    src_playlist = src_repo.find_playlist_by_id(src_playlist_id)
    dst_playlist = find_corresponding_playlist(src_playlist, dst_repo.find_playlists())
    return dst_repo.find_tracks(dst_playlist.id) if dst_playlist else []


def find_corresponding_playlist(
    src_playlist: Playlist, dst_playlists: list[Playlist]
) -> Optional[Playlist]:
    return next((p for p in dst_playlists if src_playlist.name == p.name), None)


def build_track_suggestions_for(
    src_track: Track, dst_repo: MusicRepository, existing_tracks: list[Track]
):
    suggestions = dst_repo.search_matching_tracks(src_track, limit=5)
    in_library = [s.id for s in suggestions if s in existing_tracks]
    return TrackSuggestions(
        target=src_track, suggestions=suggestions, in_library=in_library
    )
