from montag.models import Playlist
from montag.repositories.ytmusic import YouTubeMusicRepo
from ytmusicapi import YTMusic
from tests.helpers import mock, resource


def test_find_playlists():
    client = mock(YTMusic, get_library_playlists=resource("ytmusic/my_playlists.json"))
    repo = YouTubeMusicRepo(client)

    playlists = repo.find_playlists()

    assert playlists == [
        Playlist(name="Your Likes", id="LM"),
        Playlist(name="Test Playlist 1", id="PLVUD6HCAOnsHaSO5FwX-tyiEy7XpWmx5M"),
        Playlist(name="Chill Mix", id="RDTMAK5uy_k4EXFD03ox0jMzIP4NNPhl2wbxA1Wa9OM"),
    ]
