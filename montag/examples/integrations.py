import json

from montag.clients.spotify import AuthToken, SpotifyClient
from montag.repositories.spotify import SpotifyRepo
from montag.repositories.ytmusic import YouTubeMusicRepo
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


def spotify_client() -> SpotifyClient:
    """Loads the access token from the file system and initializes the client with it."""
    with open(SPOTIFY_TOKEN_FILE, "r") as f:
        auth_token = AuthToken(**json.load(f))
        return SpotifyClient(auth_token=auth_token)


def spotify_repo() -> SpotifyRepo:
    return SpotifyRepo(client=spotify_client())


def ytmusic_client():
    return YTMusic("tmp/ytmusic_auth.json")


def ytmusic_repo():
    return YouTubeMusicRepo(ytmusic_client())
