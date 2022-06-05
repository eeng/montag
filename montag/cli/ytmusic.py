from typing import Optional

import click
from ytmusicapi import YTMusic

AUTH_FILE = "tmp/ytmusic_auth.json"


def read_auth_token() -> Optional[str]:
    try:
        with open(AUTH_FILE, "r") as f:
            return f.read()
    except:
        return None


@click.command()
def auth_ytmusic():
    """Runs the YTMusic authorization flow"""

    MARKER = (
        "# Please paste above browser headers as explanied here:"
        "https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers\n"
    )
    message = click.edit("\n\n" + MARKER) or ""
    headers = message.split(MARKER, 1)[0].rstrip("\n")

    if not headers:
        click.secho("No headers found.", fg="red")
        return

    try:
        YTMusic.setup(headers_raw=headers, filepath=AUTH_FILE)
        click.secho(f"Done! Token saved to {AUTH_FILE}", fg="green")
    except Exception as err:
        click.secho(str(err), fg="red")
