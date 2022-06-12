from typing import Optional

import click
from montag.cli import spotify, ytmusic
from montag.cli.support import handle_response
from montag.domain.entities import (
    Playlist,
    PlaylistId,
    Provider,
    SuggestedTrack,
    Track,
    TrackId,
    TrackSuggestions,
)
from montag.system import System
from montag.use_cases.add_tracks_to_playlist import AddTracksToPlaylist
from montag.use_cases.create_playlist import CreatePlaylist
from montag.use_cases.fetch_tracks import FetchTracks
from montag.use_cases.search_matching_tracks import SearchMatchingTracks


def system() -> System:
    return System.build(
        spotify_auth_token=spotify.read_auth_token(),
        spotify_on_token_expired=spotify.write_auth_token,
        ytmusic_auth_token=ytmusic.read_auth_token(),
    )


def display_playlist(playlist):
    playlist_id = click.style(playlist.id, dim=True)
    playlist_name = click.style(playlist.name, bold=True)
    click.echo(f"{playlist_name} {playlist_id}")


@click.command()
@click.argument("provider", type=Provider)
def fetch_playlists(provider: Provider):
    """Retrieve all the playlist in the provider"""

    response = system().fetch_playlists(provider)

    def on_success(playlists: list[Playlist]):
        for playlist in playlists:
            display_playlist(playlist)

    handle_response(response, on_success)


@click.command()
@click.argument("provider", type=Provider)
@click.argument("playlist_name", type=str)
def create_playlist(**params):
    """Add a new playlist to a provider"""

    request = CreatePlaylist.Request(**params)
    response = system().create_playlist(request)

    def on_success(playlist: Playlist):
        click.secho("Playlist created!", fg="green")
        display_playlist(playlist)

    handle_response(response, on_success)


def format_track(track: Track, name_color: Optional[str] = None) -> str:
    track_id = click.style(track.id, dim=True)
    track_name = click.style(track.name, fg=name_color, bold=True)
    artist = click.style(", ".join(track.artists), bold=True)
    return click.style(f"{track_name} from {artist} of album {track.album} {track_id}")


@click.command()
@click.argument("provider", type=Provider)
@click.argument("playlist-id", type=PlaylistId)
def fetch_tracks(**params):
    """Gets all tracks in the specified playlist_id of the provider"""

    request = FetchTracks.Request(**params)
    response = system().fetch_tracks(request)

    def on_success(tracks: list[Track]):
        for track in tracks:
            click.echo(format_track(track, name_color="green"))

    handle_response(response, on_success)


@click.command()
@click.argument("provider", type=Provider)
@click.argument("playlist-id", type=PlaylistId)
@click.option("-t", "--track-ids", type=TrackId, required=True, multiple=True)
def add_tracks(**params):
    """Add one or more tracks to the specified playlist"""

    request = AddTracksToPlaylist.Request(**params)
    response = system().add_tracks_to_playlist(request)

    def on_success(_):
        click.secho("Done!", fg="green")

    handle_response(response, on_success)


def display_target_track(track: Track):
    click.echo(f"\nSuggestions for {format_track(track, name_color='yellow')}:")


def display_suggested_track(suggestion: SuggestedTrack):
    track_color = "cyan" if suggestion.already_present else "blue"
    click.echo(" " * 3 + format_track(suggestion, track_color))


def display_suggestions(track_suggestions: TrackSuggestions):
    display_target_track(track_suggestions.target)

    for suggestion in track_suggestions.suggestions:
        display_suggested_track(suggestion)


def add_suggestion(
    track_suggestions: TrackSuggestions,
    provider: Provider,
    playlist_id: PlaylistId,
    dry_run: bool,
):
    if track_suggestions.is_some_already_present:
        click.echo("Track already in destination, ignoring.")
    else:
        new_track = track_suggestions.suggestions[0]
        click.secho(f"Adding track {format_track(new_track, name_color='green')}")

        if not dry_run:
            request = AddTracksToPlaylist.Request(
                provider=provider, playlist_id=playlist_id, track_ids=[new_track.id]
            )
            response = system().add_tracks_to_playlist(request)

            def on_success(_):
                click.secho("Done!", fg="green")

            handle_response(response, on_success=on_success)


@click.command()
@click.argument("src_provider", type=Provider)
@click.argument("src_playlist_id", type=PlaylistId)
@click.argument("dst_provider", type=Provider)
@click.argument("dst_playlist_id", type=PlaylistId)
@click.option("-l", "--max-suggestions", type=int, default=3, show_default=True)
@click.option("-d", "--dry-run", type=bool, default=False, is_flag=True)
def replicate_playlist(
    src_provider: Provider,
    src_playlist_id: PlaylistId,
    dst_provider: Provider,
    dst_playlist_id: PlaylistId,
    max_suggestions: int,
    dry_run: bool,
):
    """Copy an entire playlist from one provider to another"""

    click.echo(f"Searching for matching tracks ...")

    request = SearchMatchingTracks.Request(
        src_provider=src_provider,
        src_playlist_id=src_playlist_id,
        dst_provider=dst_provider,
        max_suggestions=max_suggestions,
    )
    response = system().search_matching_tracks(request)

    def on_success(tracks_suggestions: list[TrackSuggestions]):
        for track_suggestions in tracks_suggestions:
            if track_suggestions.suggestions:
                display_suggestions(track_suggestions)
                add_suggestion(track_suggestions, dst_provider, dst_playlist_id, dry_run)
            else:
                click.secho("No suggestions found.", fg="magenta")

    handle_response(response, on_success)
