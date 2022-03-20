import json

from montag.clients.spotify_client import AuthToken, SpotifyClient

SPOTIFY_TOKEN_FILE = "tmp/spotify_token.json"


def run_spotify_auth_flow():
    """Runs the authorization flow to obtain an access token and stores in in the file system."""
    client = SpotifyClient()
    url, _ = client.authorize_url_and_state()
    code = input(f"Open {url} and then paste code here:\n")
    auth_token = client.request_access_token(code)
    with open(SPOTIFY_TOKEN_FILE, "w") as f:
        json.dump(auth_token.dict(), f)


def read_spotify_auth_token() -> AuthToken:
    """Loads the access token from the file system."""
    with open(SPOTIFY_TOKEN_FILE, "r") as f:
        return AuthToken(**json.load(f))
