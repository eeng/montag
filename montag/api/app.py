from flask import Flask, abort, redirect, request, url_for
from montag.gateways.spotify import SpotifyClient

SPOTIFY_STATE_KEY = "spotify_auth_state"

app = Flask(__name__)
spotify_client = SpotifyClient()


@app.route("/")
def index():
    return f"<a href='{url_for('.spotify_login')}'>Login to Spotify</a>"


@app.route("/spotify/login")
def spotify_login():
    url, state = spotify_client.authorize_url_and_state()
    response = redirect(url)
    response.set_cookie(SPOTIFY_STATE_KEY, state)
    return response


@app.route("/spotify/callback")
def spotify_callback():
    sent_state = request.cookies.get(SPOTIFY_STATE_KEY)
    received_state = request.args.get("state")

    if sent_state == received_state:
        code = request.args.get("code")
        response = spotify_client.request_access_token(code)
        return f"{response}"
    else:
        abort(403, description="Something went wrong during Spotify authorization")
