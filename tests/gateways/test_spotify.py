from unittest.mock import Mock
from callee import Attrs, Dict
import pytest
from montag.gateways.spotify import (
    AuthToken,
    SpotifyClient,
    NotAuthorizedError,
    BadRequestError,
)
from tests.helpers import HasEntry, fake_clock, mock_http_adapter, resource
from tests import factory

AUTH_TOKEN = factory.auth_token()


def test_authorize_url_and_state():
    client = SpotifyClient(
        client_id="FAKE_CLIENT_ID",
        client_secret="FAKE_CLIENT_SECRET",
        redirect_uri="FAKE_REDIRECT_URL",
    )

    actual_url, state = client.authorize_url_and_state()

    expected_url = (
        "https://accounts.spotify.com/authorize?"
        "client_id=FAKE_CLIENT_ID&"
        "redirect_uri=FAKE_REDIRECT_URL&"
        f"state={state}&"
        "scope=user-read-private+user-read-email+user-library-read&"
        "response_type=code"
    )
    assert actual_url == expected_url


def test_state_changes_with_every_call():
    client = SpotifyClient()
    _, state1 = client.authorize_url_and_state()
    _, state2 = client.authorize_url_and_state()
    assert state1 != state2


def test_request_access_token():
    response = resource("responses/access_token.json")
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


def test_refresh_access_token():
    response = resource("responses/refreshed_token.json")
    http_adapter = mock_http_adapter(post=response)
    clock = fake_clock(timestamp=1647160000)
    client = SpotifyClient(
        auth_token=AUTH_TOKEN,
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
            refresh_token=AUTH_TOKEN.refresh_token,
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
        ),
    )
    assert auth_token == AuthToken(
        refresh_token=AUTH_TOKEN.refresh_token,
        access_token=response["access_token"],
        expires_at=1647163600,
    )
    assert client.auth_token == auth_token


def test_me():
    response = resource("responses/me.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=AUTH_TOKEN, http_adapter=http_adapter)

    profile = client.me()

    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {AUTH_TOKEN.access_token}"},
    )
    assert profile == response


def test_me_requires_authorization():
    with pytest.raises(NotAuthorizedError):
        SpotifyClient().me()


def test_bad_request_error():
    response = resource("responses/token_expired.json")
    http_adapter = mock_http_adapter(get=response)

    client = SpotifyClient(auth_token=AUTH_TOKEN, http_adapter=http_adapter)
    with pytest.raises(BadRequestError):
        client.me()


def test_token_expiration():
    """Should refresh the token and notify the on_token_expired callback"""

    new_token_response = resource("responses/refreshed_token.json")
    me_response = resource("responses/me.json")
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
        data=HasEntry("grant_type", "refresh_token"),
    )
    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me", headers=Dict()
    )
    on_token_expired.assert_called_once_with(
        Attrs(access_token=new_token_response["access_token"])
    )


def test_my_playlists():
    response = resource("responses/my_playlists.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=AUTH_TOKEN, http_adapter=http_adapter)

    playlists = client.my_playlists(limit=5, offset=10)

    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me/playlists",
        params={"limit": 5, "offset": 10},
        headers={"Authorization": f"Bearer {AUTH_TOKEN.access_token}"},
    )
    assert playlists == response


def test_my_tracks():
    response = resource("responses/my_tracks.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=AUTH_TOKEN, http_adapter=http_adapter)

    tracks = client.my_tracks(limit=5, offset=10)

    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me/tracks",
        params={"limit": 5, "offset": 10},
        headers={"Authorization": f"Bearer {AUTH_TOKEN.access_token}"},
    )
    assert tracks == response
