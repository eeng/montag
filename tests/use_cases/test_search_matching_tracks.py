from unittest.mock import call

import pytest
from montag.domain import Provider
from montag.repositories.types import MusicRepository
from montag.use_cases.search_matching_tracks import (
    SearchMatchingTracks,
    SearchMatchingTracksRequest,
    TrackSuggestions,
)
from tests import factory
from tests.helpers import mock


@pytest.fixture
def spotify_repo():
    return mock(MusicRepository)


@pytest.fixture
def ytmusic_repo():
    return mock(MusicRepository)


@pytest.fixture
def use_case(spotify_repo, ytmusic_repo):
    repos: dict[Provider, MusicRepository] = {
        Provider.SPOTIFY: spotify_repo,
        Provider.YT_MUSIC: ytmusic_repo,
    }
    return SearchMatchingTracks(repos)


def test_search_tracks_matching_the_ones_in_the_src_playlist(
    use_case, spotify_repo, ytmusic_repo
):
    playlist_id = "PLVUD"
    track1, track2 = factory.track(name="T1"), factory.track(name="T2")
    track1_suggestions = factory.tracks(2, name="For T1")
    track2_suggestions = factory.tracks(3, name="For T2")

    spotify_repo.find_tracks.return_value = [track1, track2]
    ytmusic_repo.search_matching_tracks.side_effect = [
        track1_suggestions,
        track2_suggestions,
    ]

    request = SearchMatchingTracksRequest(
        src_playlist_id=playlist_id,
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
    )
    response = use_case.run(request)

    assert response.value == [
        TrackSuggestions(
            target=track1, suggestions=track1_suggestions, already_present=[]
        ),
        TrackSuggestions(
            target=track2, suggestions=track2_suggestions, already_present=[]
        ),
    ]
    spotify_repo.find_tracks.assert_called_once_with(playlist_id)
    ytmusic_repo.search_matching_tracks.assert_has_calls(
        [call(track1, limit=5), call(track2, limit=5)]
    )


def test_when_a_track_already_exists_in_dst_playlist(
    use_case, spotify_repo, ytmusic_repo
):
    spotify_playlist = factory.playlist(name="Classics")
    ytmusic_playlist = factory.playlist(name="Classics")

    src_track = factory.track(name="T1")
    dst_t1, dst_t2, dst_t3 = [
        factory.track(name="S1"),
        factory.track(name="S2"),
        factory.track(name="S3"),
    ]

    spotify_repo.find_playlist_by_id.return_value = spotify_playlist
    spotify_repo.find_tracks.return_value = [src_track]

    ytmusic_repo.find_playlist_like.return_value = ytmusic_playlist
    ytmusic_repo.find_tracks.return_value = [dst_t1, dst_t3]
    ytmusic_repo.search_matching_tracks.return_value = [dst_t1, dst_t2]

    request = SearchMatchingTracksRequest(
        src_playlist_id=spotify_playlist.id,
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
    )
    response = use_case.run(request)

    assert response.value == [
        TrackSuggestions(
            target=src_track, suggestions=[dst_t1, dst_t2], already_present=[dst_t1.id]
        )
    ]
    ytmusic_repo.find_tracks.assert_called_once_with(ytmusic_playlist.id)
