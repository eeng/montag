from typing import Callable

import click
from montag.use_cases.types import Response, Success, T


def handle_response(response: Response[T], on_success: Callable[[T], None]):
    if isinstance(response, Success):
        on_success(response.value)
    else:
        click.secho(response.msg, fg="red")
