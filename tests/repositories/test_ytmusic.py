from montag.domain import Playlist, Track
from montag.repositories.ytmusic import YouTubeMusicRepo
from ytmusicapi import YTMusic
from tests.helpers import mock, resource


def test_find_playlists():
    client = mock(
        YTMusic, get_library_playlists=resource("ytmusic/get_library_playlists.json")
    )
    repo = YouTubeMusicRepo(client)

    playlists = repo.find_playlists()

    assert playlists == [
        Playlist(name="Your Likes", id="LM"),
        Playlist(name="Test Playlist 1", id="PLVUD6HCAOnsHaSO5FwX-tyiEy7XpWmx5M"),
        Playlist(name="Chill Mix", id="RDTMAK5uy_k4EXFD03ox0jMzIP4NNPhl2wbxA1Wa9OM"),
    ]


def test_find_tracks_in_playlist():
    client = mock(YTMusic, get_playlist=resource("ytmusic/get_playlist.json"))
    repo = YouTubeMusicRepo(client)

    playlists = repo.find_tracks(playlist_id="LM")

    assert playlists == [
        Track(id="qG6_d9tpR84", name="Zombie", album="Disobey", artists=["Bad Wolves"]),
        Track(id="6tsW4ik73ac", name="No More", album=None, artists=["Disturbed"]),
    ]
    client.get_playlist.assert_called_with(playlistId="LM")
