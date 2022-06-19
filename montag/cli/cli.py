import click
from montag.cli import core, spotify, ytmusic


@click.group()
def cli():
    pass


cli.add_command(spotify.auth_spotify)
cli.add_command(ytmusic.auth_ytmusic)
cli.add_command(core.get_providers)
cli.add_command(core.get_playlists)
cli.add_command(core.create_playlist)
cli.add_command(core.get_tracks)
cli.add_command(core.add_tracks)
cli.add_command(core.replicate_playlist)

if __name__ == "__main__":
    cli()
