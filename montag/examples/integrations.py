from dataclasses import dataclass
import json

from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.domain import Provider
from montag.repositories.spotify_repo import SpotifyRepo
from montag.repositories.music_repo import MusicRepo
from montag.repositories.ytmusic_repo import YouTubeMusicRepo
from ytmusicapi import YTMusic

SPOTIFY_TOKEN_FILE = "tmp/spotify_token.json"


def run_spotify_auth_flow() -> SpotifyClient:
    """Does the authorization flow to obtain an access token."""
    client = SpotifyClient()
    url, _ = client.authorize_url_and_state()
    code = input(f"Open {url} and then paste code here:\n")
    auth_token = client.request_access_token(code)
    with open(SPOTIFY_TOKEN_FILE, "w") as f:
        json.dump(auth_token.dict(), f)
    return client


def build_spotify_client() -> SpotifyClient:
    """Loads the access token from the file system and initializes the client with it."""
    with open(SPOTIFY_TOKEN_FILE, "r") as f:
        auth_token = AuthToken(**json.load(f))
        return SpotifyClient(auth_token=auth_token)


@dataclass
class System:
    spotify_client: SpotifyClient
    spotify_repo: SpotifyRepo
    ytmusic_client: YTMusic
    ytmusic_repo: YouTubeMusicRepo
    repos: dict[Provider, MusicRepo]


def build_system() -> System:
    spotify_client = build_spotify_client()
    spotify_repo = SpotifyRepo(client=spotify_client)
    ytmusic_client = YTMusic("tmp/ytmusic_auth.json")
    ytmusic_repo = YouTubeMusicRepo(ytmusic_client)
    repos = {
        Provider.SPOTIFY: spotify_repo,
        Provider.YT_MUSIC: ytmusic_repo,
    }
    return System(
        spotify_client=spotify_client,
        spotify_repo=spotify_repo,
        ytmusic_client=ytmusic_client,
        ytmusic_repo=ytmusic_repo,
        repos=repos,
    )
