import json

from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.domain.entities import Provider
from montag.system import System
from montag.use_cases.add_tracks_to_playlist import AddTracksToPlaylist
from montag.use_cases.fetch_playlists import FetchPlaylists
from montag.use_cases.search_matching_tracks import SearchMatchingTracks


SPOTIFY_TOKEN_FILE = "tmp/spotify_token.json"
YTMUSIC_AUTH_FILE = "tmp/ytmusic_auth.json"


def write_spotify_auth_token(auth_token: AuthToken):
    with open(SPOTIFY_TOKEN_FILE, "w") as f:
        json.dump(auth_token.dict(), f)


def read_spotify_auth_token() -> AuthToken:
    with open(SPOTIFY_TOKEN_FILE, "r") as f:
        return AuthToken(**json.load(f))


def run_spotify_auth_flow():
    """Runs the authorization flow to obtain an access token and stores in in the file system."""
    client = SpotifyClient()
    url = client.authorize_url()
    code = input(f"Open {url} and then paste code here:\n")
    auth_token = client.request_access_token(code)
    write_spotify_auth_token(auth_token)


def read_ytmusic_auth_token() -> str:
    with open(YTMUSIC_AUTH_FILE, "r") as f:
        return f.read()


def system():
    return System.build(
        spotify_auth_token=read_spotify_auth_token(),
        spotify_on_token_expired=write_spotify_auth_token,
        ytmusic_auth_token=read_ytmusic_auth_token(),
    )


def examples():
    system().fetch_playlists_use_case.execute(Provider.SPOTIFY)

    request = SearchMatchingTracks.Request(
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
        src_playlist_id="6bMoQmuO8h4LuoiREgyYbZ",
    )
    SearchMatchingTracks(system().repos).execute(request)

    FetchPlaylists(system().repos).execute(Provider.YT_MUSIC)

    request = AddTracksToPlaylist.Request(
        provider=Provider.YT_MUSIC,
        playlist_id="PLVUD6HCAOnsGu80MGY1bJ1raMwtbOv75Y",
        track_ids=["f4kXLlFEFTw", "qQ0zxuWFxrY"],
    )
    AddTracksToPlaylist(system().repos).execute(request)
