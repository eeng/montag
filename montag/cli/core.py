import click
from montag.cli import spotify, ytmusic
from montag.cli.support import handle_response
from montag.domain.entities import Playlist, PlaylistId, Provider, TrackSuggestions
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

    def on_success(playlists: list[Playlist]):
        for playlist in playlists:
            playlist_id = click.style(playlist.id, dim=True)
            playlist_name = click.style(playlist.name, bold=True)
            click.echo(f"{playlist_name} {playlist_id}")

    handle_response(response, on_success)


@click.command()
@click.argument("src_provider", type=Provider)
@click.argument("dst_provider", type=Provider)
@click.argument("src_playlist_id", type=PlaylistId)
@click.option("-l", "--max-suggestions", type=int, default=3, show_default=True)
def search_matching_tracks(**params):
    click.echo(f"Searching for matching tracks ...")

    request = SearchMatchingTracks.Request(**params)
    response = system().search_matching_tracks_use_case.execute(request)

    def on_success(tracks_suggestions: list[TrackSuggestions]):
        for track_suggestions in tracks_suggestions:
            target = track_suggestions.target
            track_name = click.style(target.name, bold=True, fg="yellow")
            artist = click.style(" ".join(target.artists), bold=True)
            click.echo(f"\nSuggestions for {track_name} from {artist} ({target.album}):")

            for suggestion in track_suggestions.suggestions:
                track_id = click.style(suggestion.id, dim=True)
                track_color = "green" if suggestion.already_present else "cyan"
                track_name = click.style(suggestion.name, fg=track_color)
                artist = click.style(", ".join(suggestion.artists), bold=True)
                click.echo(f"{track_id} {track_name} from {artist} ({suggestion.album})")

    handle_response(response, on_success)
