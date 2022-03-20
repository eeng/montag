from montag.domain import Provider
from montag.use_cases.fetch_playlists import FetchPlaylists
from tests import factory


def test_fetch_playlists(repos, spotify_repo):
    expected_playlists = factory.playlists(2)
    spotify_repo.find_playlists.return_value = expected_playlists

    response = FetchPlaylists(repos).execute(Provider.SPOTIFY)

    assert response.value == expected_playlists


# TODO Error handling
