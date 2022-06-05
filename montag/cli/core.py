from email.policy import default
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
    TrackSuggestions,
)
from montag.system import System
from montag.use_cases.create_playlist import CreatePlaylist
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
    "Retrieve all the playlist in the provider"

    response = system().fetch_playlists(provider)

    def on_success(playlists: list[Playlist]):
        for playlist in playlists:
            display_playlist(playlist)

    handle_response(response, on_success)


@click.command()
@click.argument("provider", type=Provider)
@click.argument("playlist_name", type=str)
def create_playlist(**params):
    "Add a new playlist to a provider"

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


def display_target_track(track: Track):
    click.echo(f"\nSuggestions for {format_track(track, name_color='yellow')}:")


def display_suggested_track(suggestion: SuggestedTrack):
    track_color = "cyan" if suggestion.already_present else "blue"
    click.echo(" " * 3 + format_track(suggestion, track_color))


def display_suggestions(track_suggestions: TrackSuggestions):
    display_target_track(track_suggestions.target)

    for suggestion in track_suggestions.suggestions:
        display_suggested_track(suggestion)


def add_recommended_track(track_suggestions: TrackSuggestions, dry_run: bool):
    some_suggestion_already_added = any([s.already_present for s in track_suggestions.suggestions])

    if some_suggestion_already_added:
        click.secho("Ignoring since one of these suggestions already exists in the playlist")
    else:
        new_track = track_suggestions.suggestions[0]
        click.echo(f"Adding track {format_track(new_track, name_color='green')}")

        if not dry_run:
            pass


@click.command()
@click.argument("src_provider", type=Provider)
@click.argument("dst_provider", type=Provider)
@click.argument("src_playlist_id", type=PlaylistId)
@click.option("-l", "--max-suggestions", type=int, default=3, show_default=True)
@click.option("-d", "--dry-run", type=bool, is_flag=True)
def replicate_playlist(dry_run: bool, **params):
    "Copy songs from the src to the dst playlist"

    click.echo(f"Searching for matching tracks ...")

    request = SearchMatchingTracks.Request(**params)
    response = system().search_matching_tracks(request)

    def on_success(tracks_suggestions: list[TrackSuggestions]):
        for track_suggestions in tracks_suggestions:
            if track_suggestions.suggestions:
                display_suggestions(track_suggestions)
                add_recommended_track(track_suggestions, dry_run=dry_run)
            else:
                click.secho("No suggestions found.", fg="magenta")

    handle_response(response, on_success)
