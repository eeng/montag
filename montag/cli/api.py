import click
from montag.cli import spotify, ytmusic
from montag.domain.entities import Provider
from montag.system import System
from montag.use_cases.types import Success


def system() -> System:
    return System.build(
        spotify_auth_token=spotify.read_auth_token(),
        spotify_on_token_expired=spotify.write_auth_token,
        ytmusic_auth_token=ytmusic.read_auth_token(),
    )


@click.command()
@click.argument("provider", type=Provider)
def fetch_playlists(provider: Provider):
    response = system().fetch_playlists_use_case.execute(provider)
    # TODO don't like this, and how to handle errors like unauthenticated?
    if isinstance(response, Success):
        for playlist in response.value:
            playlist_id = click.style(playlist.id, dim=True)
            playlist_name = click.style(playlist.name, bold=True)
            click.echo(f"{playlist_name} {playlist_id}")
