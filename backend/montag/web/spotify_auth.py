import secrets
from typing import Optional

from flask import Blueprint, g, redirect, request, session
from montag.clients.spotify_client import AuthToken
from montag.web.support import system

AUTH_STATE_SESSION_KEY = "spotify_auth_state"
AUTH_TOKEN_SESSION_KEY = "spotify_auth_token"


bp = Blueprint("spotify", __name__, url_prefix="/spotify")


@bp.route("/login")
def spotify_login():
    state = secrets.token_hex(8)
    url = system().spotify_client.authorize_url(state)
    redirect_to = request.args["redirect_to"]
    session[AUTH_STATE_SESSION_KEY] = (state, redirect_to)
    return redirect(url)


@bp.route("/callback")
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


def store_auth_token(auth_token: AuthToken):
    session[AUTH_TOKEN_SESSION_KEY] = auth_token.dict()


def fetch_auth_token() -> Optional[AuthToken]:
    auth_token_attrs = session.get(AUTH_TOKEN_SESSION_KEY)
    if auth_token_attrs:
        return AuthToken(**auth_token_attrs)
    return None


@bp.before_app_request
def set_spotify_client_opts():
    g.spotify_fetch_auth_token = fetch_auth_token
    g.spotify_on_token_expired = store_auth_token


def is_spotify_authorized():
    return session.get(AUTH_TOKEN_SESSION_KEY) is not None
