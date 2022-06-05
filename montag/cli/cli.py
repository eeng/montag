import click
from montag.cli import core, spotify, ytmusic


@click.group()
def cli():
    pass


cli.add_command(spotify.auth_spotify)
cli.add_command(ytmusic.auth_ytmusic)
cli.add_command(core.fetch_playlists)
cli.add_command(core.replicate_playlist)
cli.add_command(core.create_playlist)

if __name__ == "__main__":
    cli()
