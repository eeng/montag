from montag.domain.entities import Provider
from montag.use_cases.add_tracks_to_playlist import AddTracksToPlaylist
from montag.use_cases.support import Success
from tests import factory


def test_add_tracks_to_playlist(repos, spotify_repo):
    playlist = factory.playlist()
    track_ids = [t.id for t in factory.tracks(2)]

    request = AddTracksToPlaylist.Request(
        provider=Provider.SPOTIFY, playlist_id=playlist.id, track_ids=track_ids
    )
    response = AddTracksToPlaylist(repos).execute(request)

    spotify_repo.add_tracks.assert_called_once_with(playlist.id, track_ids)
    assert response == Success(None)
