import logging
from typing import Callable

import click
from montag.cli import spotify, ytmusic
from montag.system import System
from montag.use_cases.support import Response, Success, T


def system() -> System:
    return System.build(
        spotify_auth_token=spotify.read_auth_token(),
        spotify_on_token_expired=spotify.write_auth_token,
        ytmusic_auth_token=ytmusic.read_auth_token(),
    )


def handle_response(response: Response[T], on_success: Callable[[T], None]):
    if isinstance(response, Success):
        on_success(response.value)
    else:
        if response.exception:
            logging.exception("Failed response", exc_info=response.exception)
        click.secho(response.msg, fg="red")
