from unittest.mock import call

import pytest
from montag.domain import Provider
from montag.repositories import MusicRepository
from montag.use_cases.search_matching_tracks import (
    SearchMatchingTracks,
    SearchMatchingTracksRequest,
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


def test_search_tracks_matching_the_src_ones(use_case, spotify_repo, ytmusic_repo):
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
        (track1, track1_suggestions),
        (track2, track2_suggestions),
    ]
    spotify_repo.find_tracks.assert_called_once_with(playlist_id)
    ytmusic_repo.search_matching_tracks.assert_has_calls(
        [call(track1, limit=5), call(track2, limit=5)]
    )
