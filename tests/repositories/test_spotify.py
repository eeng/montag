from montag.clients.spotify import SpotifyClient
from montag.domain import Playlist, Track
from montag.repositories.spotify import SpotifyRepo
from tests.helpers import mock, resource
from tests.matchers import has_attrs


def test_find_tracks_in_the_liked_songs_playlist():
    client = mock(SpotifyClient, liked_tracks=resource("spotify/liked_tracks.json"))
    repo = SpotifyRepo(client)

    tracks = repo.find_tracks(playlist_id="LS")

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


def test_find_tracks_in_another_playlist():
    client = mock(
        SpotifyClient, playlist_tracks=resource("spotify/playlist_tracks.json")
    )
    repo = SpotifyRepo(client)
    playlist_id = "37i9dQZF1DX4E3UdUs7fUx"

    tracks = repo.find_tracks(playlist_id=playlist_id)

    assert [
        has_attrs(name="Lamento Boliviano"),
        has_attrs(name="La chispa adecuada"),
    ] == tracks
    client.playlist_tracks.assert_called_with(playlist_id, limit=50, offset=0)


def test_find_playlists():
    client = mock(SpotifyClient, my_playlists=resource("spotify/my_playlists.json"))
    repo = SpotifyRepo(client)

    playlists = repo.find_playlists()

    assert playlists == [
        Playlist(name="Liked Songs", id="LS"),
        Playlist(name="My Shazam Tracks", id="5m7aOK7YN9oZy9cufeauD3"),
        Playlist(name="Soundtracks", id="4Rd2URtKmEhvcSr8wtltfs"),
        Playlist(name="Rock Classics", id="3ODmycCuoBkIccAREsJjFM"),
    ]
    client.my_playlists.assert_called_once()
