import json

from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.domain.entities import Provider
from montag.system import System
from montag.use_cases.fetch_playlists import FetchPlaylists
from montag.use_cases.search_matching_tracks import (
    SearchMatchingTracks,
    SearchMatchingTracksRequest,
)

SPOTIFY_TOKEN_FILE = "tmp/spotify_token.json"


def run_spotify_auth_flow():
    """Runs the authorization flow to obtain an access token and stores in in the file system."""
    client = SpotifyClient()
    url = client.authorize_url()
    code = input(f"Open {url} and then paste code here:\n")
    auth_token = client.request_access_token(code)
    with open(SPOTIFY_TOKEN_FILE, "w") as f:
        json.dump(auth_token.dict(), f)


def read_spotify_auth_token() -> AuthToken:
    """Loads the access token from the file system."""
    with open(SPOTIFY_TOKEN_FILE, "r") as f:
        return AuthToken(**json.load(f))


def system():
    return System.build(read_spotify_auth_token())


def examples():
    FetchPlaylists(system().repos).execute(Provider.SPOTIFY)

    request = SearchMatchingTracksRequest(
        src_playlist_id="6bMoQmuO8h4LuoiREgyYbZ",
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
    )
    SearchMatchingTracks(system().repos).execute(request)
