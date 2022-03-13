import os
from typing import Optional
from flask import Flask, abort, redirect, request, url_for, g, session
from montag.gateways.spotify import AuthToken, SpotifyClient

SPOTIFY_COOKIE_KEY = "spotify_auth_state"
SPOTIFY_SESSION_KEY = "spotify_token"

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]


@app.route("/")
def index():
    return f"<a href='{url_for('.spotify_login')}'>Login to Spotify</a>"


@app.route("/spotify/login")
def spotify_login():
    url, state = spotify_client().authorize_url_and_state()
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
        abort(403, description="Something went wrong during Spotify authorization")


@app.route("/spotify/profile")
def spotify_profile():
    return spotify_client().me()


def spotify_client():
    if "spotify_client" not in g:
        g.spotify_client = SpotifyClient(
            auth_token=retrieve_auth_token(), on_token_expired=store_auth_token
        )
        print(">>> using token", g.spotify_client.auth_token)
    return g.spotify_client


def retrieve_auth_token() -> Optional[AuthToken]:
    auth_token_attrs = session.get(SPOTIFY_SESSION_KEY)
    if auth_token_attrs:
        return AuthToken(**auth_token_attrs)
    return None


def store_auth_token(auth_token: AuthToken):
    print(">>> storing token", auth_token)
    session[SPOTIFY_SESSION_KEY] = auth_token.dict()
