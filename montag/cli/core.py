import click
from montag.cli import spotify, ytmusic
from montag.domain.entities import PlaylistId, Provider
from montag.system import System
from montag.use_cases.search_matching_tracks import SearchMatchingTracks
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


@click.command()
@click.argument("src_provider", type=Provider)
@click.argument("dst_provider", type=Provider)
@click.argument("src_playlist_id", type=PlaylistId)
@click.option("-l", "--max-suggestions", type=int, default=3, show_default=True)
def search_matching_tracks(
    src_provider: Provider,
    dst_provider: Provider,
    src_playlist_id: PlaylistId,
    max_suggestions: int,
):
    click.echo(f"Searching for matching tracks ...")

    request = SearchMatchingTracks.Request(
        src_playlist_id=src_playlist_id,
        src_provider=src_provider,
        dst_provider=dst_provider,
        max_suggestions=max_suggestions,
    )
    response = system().search_matching_tracks_use_case.execute(request)
    if isinstance(response, Success):
        for track_suggestions in response.value:
            target = track_suggestions.target
            track_name = click.style(target.name, bold=True, fg="yellow")
            artist = click.style(" ".join(target.artists), bold=True)
            click.echo(f"\nSuggestions for {track_name} from {artist} ({target.album}):")

            for suggestion in track_suggestions.suggestions:
                track_id = click.style(suggestion.id, dim=True)
                already_in_playlist = suggestion.id in track_suggestions.already_present
                track_color = "green" if already_in_playlist else "cyan"
                track_name = click.style(suggestion.name, fg=track_color)
                artist = click.style(", ".join(suggestion.artists), bold=True)
                click.echo(f"{track_id} {track_name} from {artist} ({suggestion.album})")