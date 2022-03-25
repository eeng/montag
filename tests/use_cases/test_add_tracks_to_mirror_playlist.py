from montag.domain.entities import Provider
from montag.use_cases.add_tracks_to_mirror_playlist import AddTracksToMirrorPlaylist
from montag.use_cases.types import Success
from tests import factory


def test_add_tracks_to_an_existent_playlist(repos, spotify_repo, ytmusic_repo):
    spotify_playlist = factory.playlist(name="Classics")
    ytmusic_playlist = factory.playlist(name="Classics")
    spotify_track_ids = [t.id for t in factory.tracks(2)]

    spotify_repo.find_playlist_by_id.return_value = spotify_playlist
    ytmusic_repo.find_mirror_playlist.return_value = ytmusic_playlist

    request = AddTracksToMirrorPlaylist.Request(
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
        src_playlist_id=spotify_playlist.id,
        dst_track_ids=spotify_track_ids,
    )
    response = AddTracksToMirrorPlaylist(repos).execute(request)

    ytmusic_repo.find_mirror_playlist.assert_called_once_with(spotify_playlist)
    ytmusic_repo.add_tracks.assert_called_once_with(
        ytmusic_playlist.id, spotify_track_ids
    )
    assert response == Success(None)


def test_add_tracks_to_a_new_playlist(repos, spotify_repo, ytmusic_repo):
    ...
    # TODO
