import json
from montag.adapters.spotify import SpotifyClient, AuthToken
from montag.repositories.spotify import SpotifyRepo

TOKEN_FILE = "tmp/spotify_token.json"


def run_auth_flow() -> SpotifyClient:
    """Does the authorization flow to obtain an access token."""
    client = SpotifyClient()
    url, _ = client.authorize_url_and_state()
    code = input(f"Open {url} and then paste code here:\n")
    auth_token = client.request_access_token(code)
    with open(TOKEN_FILE, "w") as f:
        json.dump(auth_token.dict(), f)
    return client


def restore_client() -> SpotifyClient:
    """Loads the access token from the file system and initializes the client with it."""
    with open("tmp/spotify_token.json", "r") as f:
        auth_token = AuthToken(**json.load(f))
        return SpotifyClient(auth_token=auth_token)


def repo() -> SpotifyRepo:
    return SpotifyRepo(client=restore_client())
