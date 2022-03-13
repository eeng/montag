from unittest.mock import Mock
from montag.models.track import Track
from montag.repositories.spotify import SpotifyRepo
from tests.helpers import resource


def test_find_all_tracks():
    client = Mock()
    client.my_tracks.return_value = resource("responses/my_tracks.json")
    repo = SpotifyRepo(client)
    tracks = repo.find_all_tracks()
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
