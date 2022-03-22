from dataclasses import dataclass

from ytmusicapi import YTMusic

from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.domain.entities import Provider
from montag.repositories.music_repo import MusicRepo
from montag.repositories.spotify_repo import SpotifyRepo
from montag.repositories.ytmusic_repo import YouTubeMusicRepo


@dataclass
class System:
    spotify_client: SpotifyClient
    spotify_repo: SpotifyRepo
    ytmusic_client: YTMusic
    ytmusic_repo: YouTubeMusicRepo
    repos: dict[Provider, MusicRepo]

    @classmethod
    def build(cls, spotify_auth_token: AuthToken):
        spotify_client = SpotifyClient(auth_token=spotify_auth_token)
        spotify_repo = SpotifyRepo(client=spotify_client)
        ytmusic_client = YTMusic("tmp/ytmusic_auth.json")
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
        )
