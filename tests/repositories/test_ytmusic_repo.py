import pytest
from montag.domain.entities import Playlist, Track
from montag.repositories.ytmusic_repo import YTMusicError, YouTubeMusicRepo
from tests import factory
from tests.helpers import mock, resource
from tests.matchers import has_attrs
from ytmusicapi import YTMusic


def test_find_playlists():
    client = mock(
        YTMusic, get_library_playlists=resource("ytmusic/get_library_playlists.json")
    )
    repo = YouTubeMusicRepo(client)

    playlists = repo.find_playlists()

    assert playlists == [
        Playlist(name="Your Likes", id="LM", is_liked=True),
        Playlist(
            name="Test Playlist 1",
            id="PLVUD6HCAOnsHaSO5FwX-tyiEy7XpWmx5M",
            is_liked=False,
        ),
        Playlist(
            name="Chill Mix",
            id="RDTMAK5uy_k4EXFD03ox0jMzIP4NNPhl2wbxA1Wa9OM",
            is_liked=False,
        ),
    ]


def test_find_tracks_in_playlist():
    client = mock(YTMusic, get_playlist=resource("ytmusic/get_playlist.json"))
    repo = YouTubeMusicRepo(client)

    playlists = repo.find_tracks(playlist_id="LM")

    client.get_playlist.assert_called_with(playlistId="LM")
    assert playlists == [
        Track(id="qG6_d9tpR84", name="Zombie", album="Disobey", artists=["Bad Wolves"]),
        Track(id="6tsW4ik73ac", name="No More", album=None, artists=["Disturbed"]),
    ]


def test_search_matching_tracks():
    client = mock(YTMusic, search=resource("ytmusic/search.json"))
    repo = YouTubeMusicRepo(client)

    tracks = repo.search_matching_tracks(
        factory.track(name="The Reason", artists=["Hoobastank"])
    )

    client.search.assert_called_once_with(
        "The Reason Hoobastank", filter="songs", limit=10
    )
    assert [
        has_attrs(name="The Reason", id="qQ0zxuWFxrY"),
        has_attrs(name="You Are The Reason", id="2Kiob5f9A1g"),
    ] == tracks


def test_create_playlist():
    playlist_id = "RDTMAK5uy_k4EXFD03ox0jMzIP4NNPhl2wbxA1Wa9OM"
    playlist_name = "Chill Mix"
    client = mock(
        YTMusic,
        create_playlist=playlist_id,
        get_library_playlists=resource("ytmusic/get_library_playlists.json"),
    )
    repo = YouTubeMusicRepo(client)

    playlist = repo.create_playlist(playlist_name)

    client.create_playlist.assert_called_once_with(playlist_name, "")
    assert playlist == Playlist(id=playlist_id, name=playlist_name)


def test_add_tracks_success():
    playlist_id = "pl"
    track_ids = ["t1", "t2"]
    client = mock(
        YTMusic, add_playlist_items=resource("ytmusic/add_playlist_items_success.json")
    )
    repo = YouTubeMusicRepo(client)

    repo.add_tracks(playlist_id, track_ids)

    client.add_playlist_items.assert_called_once_with(playlist_id, track_ids)


def test_add_tracks_failure():
    client = mock(
        YTMusic, add_playlist_items=resource("ytmusic/add_playlist_items_failure.json")
    )
    repo = YouTubeMusicRepo(client)

    with pytest.raises(YTMusicError):
        repo.add_tracks("p", ["t"])
