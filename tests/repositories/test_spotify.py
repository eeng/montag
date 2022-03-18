from montag.clients.spotify import SpotifyClient
from montag.domain import Playlist, Track
from montag.repositories.spotify import SpotifyRepo
from tests import factory
from tests.helpers import mock, resource
from tests.matchers import has_attrs


def test_find_tracks_in_liked_songs_playlist():
    client = mock(SpotifyClient, liked_tracks=resource("spotify/liked_tracks.json"))
    repo = SpotifyRepo(client)

    tracks = repo.find_tracks(playlist_id="LS")

    assert tracks == [
        Track(
            id="7vcDJCAO356RYkCfiUozmE",
            name="Maldito duende",
            album="Senderos De Traición",
            artists=["Heroes Del Silencio"],
        ),
        Track(
            id="2tkL5ggXp1EJ6ZlRagQJBA",
            name="Sell My Soul",
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

    client.playlist_tracks.assert_called_with(playlist_id, limit=50, offset=0)
    assert [
        has_attrs(name="Lamento Boliviano"),
        has_attrs(name="La chispa adecuada"),
    ] == tracks


def test_find_playlists():
    client = mock(SpotifyClient, my_playlists=resource("spotify/my_playlists.json"))
    repo = SpotifyRepo(client)

    playlists = repo.find_playlists()

    client.my_playlists.assert_called_once()
    assert playlists == [
        Playlist(name="Liked Songs", id="LS"),
        Playlist(name="My Shazam Tracks", id="5m7aOK7YN9oZy9cufeauD3"),
        Playlist(name="Soundtracks", id="4Rd2URtKmEhvcSr8wtltfs"),
        Playlist(name="Rock Classics", id="3ODmycCuoBkIccAREsJjFM"),
    ]


def test_search_tracks_matching():
    client = mock(SpotifyClient, search=resource("spotify/search.json"))
    repo = SpotifyRepo(client)

    tracks = repo.search_tracks_matching(
        factory.track(name="The Reason", artists=["Hoobastank"])
    )

    client.search.assert_called_with(
        "track:The Reason artist:Hoobastank", type="track", limit=10
    )
    assert [
        has_attrs(name="The Reason 1", id="77loZpT5Y5PRP1S451P9Yz"),
        has_attrs(name="The Reason 2", id="3e96gL2t9JYdzlVvJP3TFx"),
    ] == tracks
