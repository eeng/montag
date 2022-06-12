from montag.domain.entities import Provider
from montag.use_cases.fetch_tracks import FetchTracks
from montag.use_cases.support import Success
from tests import factory


def test_fetch_tracks(repos, spotify_repo):
    expected_tracks = factory.tracks(2)
    spotify_repo.find_tracks.return_value = expected_tracks
    playlist_id = "6bMoQmu"

    request = FetchTracks.Request(provider=Provider.SPOTIFY, playlist_id=playlist_id)
    response = FetchTracks(repos).execute(request)

    assert response == Success(expected_tracks)
    spotify_repo.find_tracks.assert_called_once_with(playlist_id)
