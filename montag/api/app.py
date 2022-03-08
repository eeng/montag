from flask import Flask, redirect, request, url_for
from montag.gateways.spotify import SpotifyClient

SPOTIFY_STATE_KEY = "spotify_auth_state"

app = Flask(__name__)


@app.route("/")
def index():
    return f"<a href='{url_for('.spotify_login')}'>Login to Spotify</a>"


@app.route("/spotify/login")
def spotify_login():
    client = SpotifyClient()
    response = redirect(client.authorize_url())
    response.set_cookie(SPOTIFY_STATE_KEY, client.state)
    return response


@app.route("/spotify/callback/")
def spotify_callback():
    return f"Args: {request.args}\nState: {request.cookies.get(SPOTIFY_STATE_KEY)}"
