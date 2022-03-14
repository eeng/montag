from unittest.mock import create_autospec
from montag.models import Playlist, Track
from montag.repositories.spotify import SpotifyClient, SpotifyRepo
from tests.helpers import resource


def test_find_tracks_without_playlist():
    client = create_autospec(SpotifyClient)
    client.liked_tracks.return_value = resource("responses/liked_tracks.json")
    repo = SpotifyRepo(client)

    tracks = repo.find_tracks()

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
    client.liked_tracks.assert_called_with(limit=50, offset=0)


def test_find_tracks_with_playlist():
    client = create_autospec(SpotifyClient)
    client.playlist_tracks.return_value = resource("responses/playlist_tracks.json")
    repo = SpotifyRepo(client)
    playlist_id = "37i9dQZF1DX4E3UdUs7fUx"

    tracks = repo.find_tracks(playlist_id=playlist_id)

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
    client.playlist_tracks.assert_called_with(playlist_id, limit=50, offset=0)


def test_find_playlists():
    client = create_autospec(SpotifyClient)
    client.my_playlists.return_value = resource("responses/my_playlists.json")
    repo = SpotifyRepo(client)

    playlists = repo.find_playlists()

    assert playlists == [
        Playlist(id="5m7aOK7YN9oZy9cufeauD3", name="My Shazam Tracks"),
        Playlist(id="4Rd2URtKmEhvcSr8wtltfs", name="Soundtracks"),
        Playlist(id="3ODmycCuoBkIccAREsJjFM", name="Rock Classics"),
    ]
    client.my_playlists.assert_called_once()
