import pytest
from montag.clients.spotify_client import BadRequestError, SpotifyClient
from montag.domain.entities import Playlist, Track
from montag.domain.errors import PlaylistNotFoundError
from montag.repositories.spotify_repo import LIKED_SONGS_ID, SpotifyRepo
from tests import factory
from tests.helpers import json_resource, mock
from tests.matchers import has_attrs


def test_find_tracks_in_liked_songs_playlist():
    client = mock(SpotifyClient, liked_tracks=json_resource("spotify/liked_tracks.json"))
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
    client = mock(SpotifyClient, playlist_tracks=json_resource("spotify/playlist_tracks.json"))
    repo = SpotifyRepo(client)
    playlist_id = "37i9dQZF1DX4E3UdUs7fUx"

    tracks = repo.find_tracks(playlist_id=playlist_id)

    client.playlist_tracks.assert_called_with(playlist_id, limit=50, offset=0)
    assert [
        has_attrs(name="Lamento Boliviano"),
        has_attrs(name="La chispa adecuada"),
    ] == tracks


def test_find_tracks_in_inexistent_playlist():
    client = mock(SpotifyClient)
    client.playlist_tracks.side_effect = BadRequestError({"status": 404})
    repo = SpotifyRepo(client)
    playlist_id = "IXCRW"

    with pytest.raises(PlaylistNotFoundError) as excinfo:
        repo.find_tracks(playlist_id=playlist_id)

    assert excinfo.value.playlist_id == playlist_id


def test_find_playlists():
    client = mock(SpotifyClient, my_playlists=json_resource("spotify/my_playlists.json"))
    repo = SpotifyRepo(client)

    playlists = repo.find_playlists()

    client.my_playlists.assert_called_once()
    assert playlists == [
        Playlist(name="Liked Songs", id="LS", is_liked=True),
        Playlist(name="My Shazam Tracks", id="5m7aOK7YN9oZy9cufeauD3", is_liked=False),
        Playlist(name="Soundtracks", id="4Rd2URtKmEhvcSr8wtltfs", is_liked=False),
        Playlist(name="Rock Classics", id="3ODmycCuoBkIccAREsJjFM", is_liked=False),
    ]


def test_search_matching_tracks():
    client = mock(SpotifyClient, search=json_resource("spotify/search.json"))
    repo = SpotifyRepo(client)

    tracks = repo.search_matching_tracks(factory.track(name="The Reason", artists=["Hoobastank"]))

    client.search.assert_called_with("track:The Reason artist:Hoobastank", type="track", limit=10)
    assert [
        has_attrs(name="The Reason 1", id="77loZpT5Y5PRP1S451P9Yz"),
        has_attrs(name="The Reason 2", id="3e96gL2t9JYdzlVvJP3TFx"),
    ] == tracks


def test_create_playlist():
    response = json_resource("spotify/create_playlist.json")
    client = mock(SpotifyClient, create_playlist=response)
    repo = SpotifyRepo(client)

    playlist = repo.create_playlist("Classics")

    client.create_playlist.assert_called_with("Classics")
    assert playlist == Playlist(id=response["id"], name=response["name"])


def test_add_tracks_to_liked_playlist():
    client = mock(SpotifyClient)
    repo = SpotifyRepo(client)
    track_ids = ["t1", "t2"]

    result = repo.add_tracks(LIKED_SONGS_ID, track_ids)

    client.add_liked_tracks.assert_called_once_with(track_ids)
    assert result == None


def test_add_tracks_to_other_playlist():
    client = mock(SpotifyClient)
    repo = SpotifyRepo(client)
    playlist_id = "u33hs5"
    track_ids = ["t1", "t2"]

    result = repo.add_tracks(playlist_id, track_ids)

    client.add_playlist_tracks.assert_called_once_with(playlist_id, track_ids)
    assert result == None
