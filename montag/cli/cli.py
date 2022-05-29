import click
from montag.cli import spotify, ytmusic, api


@click.group()
def cli():
    pass


cli.add_command(spotify.auth_spotify)
cli.add_command(ytmusic.auth_ytmusic)
cli.add_command(api.fetch_playlists)

if __name__ == "__main__":
    cli()
