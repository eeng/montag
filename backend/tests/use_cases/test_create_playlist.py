from montag.domain.entities import Provider
from montag.use_cases.create_playlist import CreatePlaylist
from montag.use_cases.types import Success
from tests import factory


def test_create_playlist(repos, spotify_repo):
    playlist = factory.playlist()
    spotify_repo.create_playlist.return_value = playlist

    request = CreatePlaylist.Request(provider=Provider.SPOTIFY, playlist_name=playlist.name)
    response = CreatePlaylist(repos).execute(request)

    spotify_repo.create_playlist.assert_called_once_with(playlist.name)
    assert response == Success(playlist)
