import secrets
from typing import Optional

from flask import Flask, g, redirect, request, session
from montag.clients.spotify_client import AuthToken
from montag.config import Config
from montag.domain.entities import Provider
from montag.system import System
from montag.use_cases.fetch_playlists import FetchPlaylists

AUTH_STATE_SESSION_KEY = "spotify_auth_state"
AUTH_TOKEN_SESSION_KEY = "spotify_auth_token"

app = Flask(__name__)
app.secret_key = Config.flask_secret_key


@app.route("/spotify/login")
def spotify_login():
    state = secrets.token_hex(8)
    url = system().spotify_client.authorize_url(state)
    redirect_to = request.args["redirect_to"]
    session[AUTH_STATE_SESSION_KEY] = (state, redirect_to)
    return redirect(url)


@app.route("/spotify/callback")
def spotify_callback():
    (sent_state, redirect_to) = session.pop(AUTH_STATE_SESSION_KEY)
    received_state = request.args.get("state")
    if sent_state == received_state:
        code = request.args["code"]
        auth_token = system().spotify_client.request_access_token(code)
        store_auth_token(auth_token)
        return redirect(redirect_to)
    else:
        # TODO what to do here?
        raise ValueError(request.args)


def system() -> System:
    if "system" not in g:
        g.system = System.build(
            spotify_auth_token=retrieve_auth_token(), spotify_on_token_expired=store_auth_token
        )
    return g.system


def store_auth_token(auth_token: AuthToken):
    session[AUTH_TOKEN_SESSION_KEY] = auth_token.dict()


def retrieve_auth_token() -> Optional[AuthToken]:
    auth_token_attrs = session.get(AUTH_TOKEN_SESSION_KEY)
    if auth_token_attrs:
        return AuthToken(**auth_token_attrs)
    return None


@app.route("/api/playlists")
def fetch_playlists():
    provider = Provider(request.args["provider"])
    response = FetchPlaylists(system().repos).execute(provider)
    return {"status": "success", "playlists": len(response.value)}
