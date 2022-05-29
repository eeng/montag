import click

from montag.cli.spotify import auth_spotify

@click.group()
def cli():
    pass

cli.add_command(auth_spotify)

if __name__ == '__main__':
  cli()
