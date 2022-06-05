import json
import os
import secrets
from multiprocessing import Process, Queue
from typing import Optional, Tuple
from urllib.parse import urlparse

import click
from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.config import Config
from werkzeug import Request, Response, run_simple

TOKEN_FILE = "tmp/spotify_token.json"


def write_auth_token(auth_token: AuthToken):
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(auth_token.dict(), f)


def read_auth_token() -> Optional[AuthToken]:
    try:
        with open(TOKEN_FILE, "r") as f:
            return AuthToken(**json.load(f))
    except:
        return None


def get_web_server_host_and_port() -> Tuple[str, int]:
    redirect_uri = urlparse(Config.spotify_redirect_uri)
    if redirect_uri.hostname is None or redirect_uri.port is None:
        raise click.UsageError("Please specify a valid SPOTIFY_REDIRECT_URI environment variable.")
    return (redirect_uri.hostname, int(redirect_uri.port))


def start_web_server_for_auth_callback(q: Queue) -> None:
    @Request.application
    def app(request: Request) -> Response:
        q.put((request.args["code"], request.args["state"]))
        return Response("Done! You can close this browser tab.", 200)

    (hostname, port) = get_web_server_host_and_port()
    run_simple(hostname, port, app)


def wait_for_auth_callback() -> Tuple[str, str]:
    callback_params_queue: Queue[Tuple[str, str]] = Queue()
    web_server = Process(target=start_web_server_for_auth_callback, args=(callback_params_queue,))
    web_server.start()
    callback_params = callback_params_queue.get(block=True)
    web_server.terminate()
    return callback_params


@click.command()
def auth_spotify():
    """Runs the Spotify authorization flow"""

    client = SpotifyClient()
    sent_state = secrets.token_hex(8)
    url = client.authorize_url(sent_state)

    click.echo("Please go to the following address to authenticate your Spotify account:\n")
    click.secho(url + "\n", bold=True)

    (code, _) = wait_for_auth_callback()

    auth_token = client.request_access_token(code)
    write_auth_token(auth_token)
    click.secho(f"Done! Token saved to {TOKEN_FILE}", fg="green")
