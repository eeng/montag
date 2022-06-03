from montag.domain.entities import Provider
from montag.use_cases.fetch_playlists import FetchPlaylists
from montag.use_cases.types import Failure, Success
from tests import factory


def test_fetch_playlists(repos, spotify_repo):
    expected_playlists = factory.playlists(2)
    spotify_repo.find_playlists.return_value = expected_playlists

    response = FetchPlaylists(repos).execute(Provider.SPOTIFY)

    assert response == Success(expected_playlists)


def test_error_handling_with_unexpected_errors(repos, spotify_repo):
    error = ValueError("some message")
    spotify_repo.find_playlists.side_effect = error

    response = FetchPlaylists(repos).execute(Provider.SPOTIFY)

    assert response == Failure("some message", error)
