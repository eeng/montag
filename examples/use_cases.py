import json

from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.domain.entities import Provider
from montag.system import System
from montag.use_cases.add_tracks_to_mirror_playlist import AddTracksToMirrorPlaylist
from montag.use_cases.fetch_playlists import FetchPlaylists
from montag.use_cases.search_matching_tracks import SearchMatchingTracks


SPOTIFY_TOKEN_FILE = "tmp/spotify_token.json"


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


def system():
    return System.build(
        spotify_auth_token=read_spotify_auth_token(),
        spotify_on_token_expired=write_spotify_auth_token,
    )


def examples():
    FetchPlaylists(system().repos).execute(Provider.SPOTIFY)

    request = SearchMatchingTracks.Request(
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
        src_playlist_id="6bMoQmuO8h4LuoiREgyYbZ",
    )
    SearchMatchingTracks(system().repos).execute(request)

    request = AddTracksToMirrorPlaylist.Request(
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
        src_playlist_id="6bMoQmuO8h4LuoiREgyYbZ",
        dst_track_ids=["f4kXLlFEFTw", "qQ0zxuWFxrY"],
    )
    AddTracksToMirrorPlaylist(system().repos).execute(request)
