# TODO remove
import secrets
from typing import Optional
from flask import Flask, g, redirect, request, session, url_for
from montag.clients.spotify_client import AuthToken, BadStateError, SpotifyClient
from montag.config import Config
from montag.repositories.spotify_repo import SpotifyRepo

SPOTIFY_COOKIE_KEY = "spotify_auth_state"
SPOTIFY_SESSION_KEY = "spotify_token"

app = Flask(__name__)
app.secret_key = Config.flask_secret_key


@app.route("/")
def index():
    return f"<a href='{url_for('.spotify_login')}'>Login to Spotify</a>"


@app.route("/spotify/login")
def spotify_login():
    state = secrets.token_hex(8)
    url = spotify_client().authorize_url(state)
    response = redirect(url)
    response.set_cookie(SPOTIFY_COOKIE_KEY, state)
    return response


@app.route("/spotify/callback")
def spotify_callback():
    sent_state = request.cookies.get(SPOTIFY_COOKIE_KEY)
    received_state = request.args.get("state")
    if sent_state == received_state:
        code = request.args["code"]
        auth_token = spotify_client().request_access_token(code)
        store_auth_token(auth_token)
        return f"{auth_token}"
    else:
        raise BadStateError(request.args)


@app.route("/spotify/profile")
def spotify_profile():
    return spotify_client().me()


@app.route("/spotify/playlists")
def spotify_playlists():
    return spotify_client().my_playlists()


@app.route("/spotify/playlists/<playlist_id>/tracks")
def spotify_tracks(playlist_id):
    return {"tracks": [track.dict() for track in spotify_repo().find_tracks(playlist_id)]}


def spotify_client():
    if "spotify_client" not in g:
        g.spotify_client = SpotifyClient(
            auth_token=retrieve_auth_token(), on_token_expired=store_auth_token
        )
    return g.spotify_client


def spotify_repo():
    return SpotifyRepo(client=spotify_client())


def retrieve_auth_token() -> Optional[AuthToken]:
    auth_token_attrs = session.get(SPOTIFY_SESSION_KEY)
    if auth_token_attrs:
        return AuthToken(**auth_token_attrs)
    return None


def store_auth_token(auth_token: AuthToken):
    session[SPOTIFY_SESSION_KEY] = auth_token.dict()
