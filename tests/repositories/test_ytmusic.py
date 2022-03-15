from montag.models import Playlist
from montag.repositories.ytmusic import YouTubeMusicClient, YouTubeMusicRepo
from tests.helpers import mock, resource


def test_find_playlists():
    client = mock(
        YouTubeMusicClient, my_playlists=resource("ytmusic/my_playlists.json")
    )
    repo = YouTubeMusicRepo(client)

    playlists = repo.find_playlists()

    assert playlists == [
        Playlist(name="Your Likes", id="LM"),
        Playlist(name="Test Playlist 1", id="PLVUD6HCAOnsHaSO5FwX-tyiEy7XpWmx5M"),
        Playlist(name="Chill Mix", id="RDTMAK5uy_k4EXFD03ox0jMzIP4NNPhl2wbxA1Wa9OM"),
    ]
    client.my_playlists.assert_called_once()
