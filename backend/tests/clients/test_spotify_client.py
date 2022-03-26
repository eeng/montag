from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from montag.clients.spotify_client import (
    AuthToken,
    BadRequestError,
    NotAuthorizedError,
    SpotifyClient,
)
from tests import factory
from tests.helpers import fake_clock, mock_http_adapter, resource
from tests.matchers import has_attrs, has_entries, instance_of


@pytest.fixture
def auth():
    token = factory.auth_token()
    return SimpleNamespace(
        token=token, header={"Authorization": f"Bearer {token.access_token}"}
    )


def test_authorize_url_and_state():
    client = SpotifyClient(
        client_id="FAKE_CLIENT_ID",
        client_secret="FAKE_CLIENT_SECRET",
        redirect_uri="FAKE_REDIRECT_URL",
    )

    actual_url = client.authorize_url("THE_STATE")

    expected_url = (
        "https://accounts.spotify.com/authorize?"
        "client_id=FAKE_CLIENT_ID&"
        "redirect_uri=FAKE_REDIRECT_URL&"
        f"state=THE_STATE&"
        "scope=user-read-private+user-read-email+user-library-read+user-library-modify+playlist-read-private+playlist-modify-private&"
        "response_type=code"
    )
    assert actual_url == expected_url


def test_request_access_token():
    response = resource("spotify/access_token.json")
    http_adapter = mock_http_adapter(post=response)
    clock = fake_clock(timestamp=1647160000)
    client = SpotifyClient(
        http_adapter=http_adapter,
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="REDIRECT_URI",
        clock=clock,
    )

    auth_token = client.request_access_token("SOME_CODE")

    http_adapter.post.assert_called_once_with(
        "https://accounts.spotify.com/api/token",
        data=dict(
            grant_type="authorization_code",
            code="SOME_CODE",
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
            redirect_uri="REDIRECT_URI",
        ),
    )
    assert auth_token == AuthToken(
        access_token=response["access_token"],
        refresh_token=response["refresh_token"],
        expires_at=1647163600,
    )
    assert client.auth_token == auth_token


def test_refresh_access_token(auth):
    response = resource("spotify/refreshed_token.json")
    http_adapter = mock_http_adapter(post=response)
    clock = fake_clock(timestamp=1647160000)
    client = SpotifyClient(
        auth_token=auth.token,
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        http_adapter=http_adapter,
        clock=clock,
    )

    auth_token = client.refresh_access_token()

    http_adapter.post.assert_called_once_with(
        "https://accounts.spotify.com/api/token",
        data=dict(
            grant_type="refresh_token",
            refresh_token=auth.token.refresh_token,
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
        ),
    )
    assert auth_token == AuthToken(
        refresh_token=auth.token.refresh_token,
        access_token=response["access_token"],
        expires_at=1647163600,
    )
    assert client.auth_token == auth_token


def test_me(auth):
    response = resource("spotify/me.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)

    profile = client.me()

    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me",
        headers=auth.header,
        params={},
    )
    assert profile == response


def test_me_requires_authorization():
    with pytest.raises(NotAuthorizedError):
        SpotifyClient().me()


def test_bad_request_error(auth):
    response = resource("spotify/token_expired.json")
    http_adapter = mock_http_adapter(get=response)

    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)
    with pytest.raises(BadRequestError):
        client.me()


def test_token_expiration():
    """Should refresh the token and notify the on_token_expired callback"""

    new_token_response = resource("spotify/refreshed_token.json")
    me_response = resource("spotify/me.json")
    http_adapter = mock_http_adapter(post=new_token_response, get=me_response)
    auth_token = factory.auth_token(expires_at=1647196101)
    on_token_expired = Mock()
    client = SpotifyClient(
        auth_token=auth_token,
        http_adapter=http_adapter,
        on_token_expired=on_token_expired,
    )
    client.me()

    http_adapter.post.assert_called_once_with(
        "https://accounts.spotify.com/api/token",
        data=has_entries(grant_type="refresh_token"),
    )
    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me", headers=instance_of(dict), params={}
    )
    on_token_expired.assert_called_once_with(
        has_attrs(access_token=new_token_response["access_token"])
    )


def test_my_playlists(auth):
    response = resource("spotify/my_playlists.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)

    playlists = client.my_playlists(limit=5, offset=10)

    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me/playlists",
        params={"limit": 5, "offset": 10},
        headers=auth.header,
    )
    assert playlists == response


def test_liked_tracks(auth):
    response = resource("spotify/liked_tracks.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)

    tracks = client.liked_tracks(limit=5, offset=10)

    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me/tracks",
        params={"limit": 5, "offset": 10},
        headers=auth.header,
    )
    assert tracks == response


def test_playlist_tracks(auth):
    response = resource("spotify/playlist_tracks.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)
    playlist_id = "6bMoQmuO8h4LuoiREgyYbZ"

    tracks = client.playlist_tracks(playlist_id)

    http_adapter.get.assert_called_once_with(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        params={"limit": 20, "offset": 0},
        headers=auth.header,
    )
    assert tracks == response


def test_search(auth):
    response = resource("spotify/search.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)

    tracks = client.search("Disturbed", type="artist")

    http_adapter.get.assert_called_once_with(
        f"https://api.spotify.com/v1/search",
        params={"q": "Disturbed", "type": "artist", "limit": 20, "offset": 0},
        headers=auth.header,
    )
    assert tracks == response


def test_create_playlist(auth):
    response = resource("spotify/create_playlist.json")
    http_adapter = mock_http_adapter(post=response, status_code=201)
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)

    playlist = client.create_playlist(name="New Playlist")

    http_adapter.post.assert_called_once_with(
        "https://api.spotify.com/v1/me/playlists",
        json={"name": "New Playlist", "public": False},
        headers=auth.header,
    )
    assert playlist == response


def test_add_liked_tracks(auth):
    http_adapter = mock_http_adapter(put="")
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)

    response = client.add_liked_tracks(["t1", "t2"])

    http_adapter.put.assert_called_once_with(
        "https://api.spotify.com/v1/me/tracks",
        json={"ids": ["t1", "t2"]},
        headers=auth.header,
    )
    assert response == None


def test_add_playlist_tracks(auth):
    playlist_id = "we34qe"
    track_ids = ["t1", "t2"]
    http_adapter = mock_http_adapter(post=resource("spotify/add_playlist_tracks.json"))
    client = SpotifyClient(auth_token=auth.token, http_adapter=http_adapter)

    response = client.add_playlist_tracks(playlist_id, track_ids)

    http_adapter.post.assert_called_once_with(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        json={"uris": ["spotify:track:t1", "spotify:track:t2"]},
        headers=auth.header,
    )
    assert response == None
