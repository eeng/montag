import json
from queue import Queue
import secrets
from threading import Thread

import click
from montag import CALLBACK_PARAMS_QUEUE
from montag.clients.spotify_client import AuthToken, SpotifyClient
from montag.web.app import create_app

SPOTIFY_TOKEN_FILE = "tmp/spotify_token.json"

def write_spotify_auth_token(auth_token: AuthToken):
    with open(SPOTIFY_TOKEN_FILE, "w") as f:
        json.dump(auth_token.dict(), f)


def read_spotify_auth_token() -> AuthToken:
    with open(SPOTIFY_TOKEN_FILE, "r") as f:
        return AuthToken(**json.load(f))

def start_web_server_to_handle_auth_redirect():
  callback_params_queue = Queue()
  app = create_app()

  def thread_target(queue):
    app.config[CALLBACK_PARAMS_QUEUE] = queue
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, load_dotenv=False)

  Thread(target=thread_target, args =(callback_params_queue, )).start()
  return callback_params_queue

@click.command()
def auth_spotify():
  """Runs the Spotify authorization flow to obtain the access token and store it in the file system."""
  client = SpotifyClient()
  sent_state = secrets.token_hex(8)
  url = client.authorize_url(sent_state)

  click.echo('Please go to the following address to authenticate your Spotify account:\n')
  click.secho(url + '\n', bold=True)

  callback_params_queue = start_web_server_to_handle_auth_redirect()

  (received_state, code) = callback_params_queue.get()

  if sent_state != received_state:
    click.secho('Wrong state', fg='red')
    return

  click.secho(code, fg='green')
  # auth_token = client.request_access_token(code)
  # write_spotify_auth_token(auth_token)
