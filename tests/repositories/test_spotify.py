from unittest.mock import Mock
from montag.models import Track
from montag.repositories.spotify import SpotifyRepo
from tests.helpers import resource


def test_find_all_tracks_without_playlist():
    client = Mock()
    client.my_tracks.return_value = resource("responses/my_tracks.json")
    repo = SpotifyRepo(client)

    tracks = repo.find_all_tracks()

    client.my_tracks.assert_called_with(limit=50, offset=0)
    assert tracks == [
        Track(
            name="Maldito duende",
            uri="spotify:track:7vcDJCAO356RYkCfiUozmE",
            album="Senderos De Traición",
            artists=["Heroes Del Silencio"],
        ),
        Track(
            name="Sell My Soul",
            uri="spotify:track:2tkL5ggXp1EJ6ZlRagQJBA",
            album="Poison The Parish",
            artists=["Seether"],
        ),
    ]


def test_find_all_tracks_with_playlist():
    client = Mock()
    client.playlist_tracks.return_value = resource("responses/playlist_tracks.json")
    repo = SpotifyRepo(client)
    playlist_id = "37i9dQZF1DX4E3UdUs7fUx"

    tracks = repo.find_all_tracks(playlist_id=playlist_id)

    client.playlist_tracks.assert_called_with(playlist_id, limit=50, offset=0)
    assert tracks == [
        Track(
            name="Maldito duende",
            uri="spotify:track:7vcDJCAO356RYkCfiUozmE",
            album="Senderos De Traición",
            artists=["Heroes Del Silencio"],
        ),
        Track(
            name="La chispa adecuada",
            uri="spotify:track:4vkSJSyPddHwL7v3l1cuRf",
            album="Avalancha",
            artists=["Heroes Del Silencio"],
        ),
    ]
