from dataclasses import dataclass
from typing import Callable, Optional

from ytmusicapi import YTMusic

from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.domain.entities import Provider
from montag.repositories.music_repo import MusicRepo
from montag.repositories.spotify_repo import SpotifyRepo
from montag.repositories.ytmusic_repo import YouTubeMusicRepo
from montag.use_cases.fetch_playlists import FetchPlaylists
from montag.use_cases.search_matching_tracks import SearchMatchingTracks


@dataclass
class System:
    spotify_client: SpotifyClient
    spotify_repo: SpotifyRepo
    ytmusic_client: YTMusic
    ytmusic_repo: YouTubeMusicRepo
    repos: dict[Provider, MusicRepo]
    fetch_playlists_use_case: FetchPlaylists
    search_matching_tracks_use_case: SearchMatchingTracks

    @classmethod
    def build(
        cls,
        spotify_auth_token: Optional[AuthToken],
        spotify_on_token_expired: Callable[[AuthToken], None],
        ytmusic_auth_token: Optional[str],
    ):
        spotify_client = SpotifyClient(
            auth_token=spotify_auth_token, on_token_expired=spotify_on_token_expired
        )
        spotify_repo = SpotifyRepo(client=spotify_client)
        ytmusic_client = YTMusic(ytmusic_auth_token or "")
        ytmusic_repo = YouTubeMusicRepo(ytmusic_client)
        repos = {
            Provider.SPOTIFY: spotify_repo,
            Provider.YT_MUSIC: ytmusic_repo,
        }
        return cls(
            spotify_client=spotify_client,
            spotify_repo=spotify_repo,
            ytmusic_client=ytmusic_client,
            ytmusic_repo=ytmusic_repo,
            repos=repos,
            fetch_playlists_use_case=FetchPlaylists(repos),
            search_matching_tracks_use_case=SearchMatchingTracks(repos),
        )
