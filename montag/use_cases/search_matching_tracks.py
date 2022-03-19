from dataclasses import dataclass
from montag.domain import PlaylistId, Provider, Track
from montag.repositories import MusicRepository
from pydantic import BaseModel

from montag.use_cases.types import Response, Ok


class SearchMatchingTracksRequest(BaseModel):
    src_provider: Provider
    src_playlist_ids: list[PlaylistId]
    dst_provider: Provider


SearchMatchingTracksResponse = Response[list[tuple[Track, list[Track]]]]


@dataclass
class SearchMatchingTracks:
    repos: dict[Provider, MusicRepository]

    def run(self, request: SearchMatchingTracksRequest) -> SearchMatchingTracksResponse:
        src_repo = self.repos[request.src_provider]
        dst_repo = self.repos[request.dst_provider]

        tracks_with_suggestions = [
            (src_track, dst_repo.search_matching_tracks(src_track, limit=5))
            for src_playlist_id in request.src_playlist_ids
            for src_track in src_repo.find_tracks(src_playlist_id)
        ]
        return Ok(tracks_with_suggestions)
