import json
import pytest
from unittest.mock import Mock
from montag.gateways.spotify import (
    SpotifyClient,
    SpotifyNotAuthorized,
    SpotifyWrongRequest,
)

AUTH_TOKEN = {"access_token": "BQDMu5", "refresh_token": "AQAXsR", "expires_in": 3600}


def test_authorize_url_and_state():
    actual_url, state = SpotifyClient(
        client_id="FAKE_CLIENT_ID",
        client_secret="FAKE_CLIENT_SECRET",
        redirect_uri="FAKE_REDIRECT_URL",
    ).authorize_url_and_state()

    expected_url = (
        "https://accounts.spotify.com/authorize?"
        "client_id=FAKE_CLIENT_ID&"
        "redirect_uri=FAKE_REDIRECT_URL&"
        f"state={state}&"
        "scope=user-read-private+user-read-email&"
        "response_type=code"
    )
    assert actual_url == expected_url


def test_state_changes_with_every_call():
    client = SpotifyClient()
    _, state1 = client.authorize_url_and_state()
    _, state2 = client.authorize_url_and_state()
    assert state1 != state2


def test_request_access_token():
    access_token_response = resource("responses/access_token.json")
    http_adapter = mock_http_adapter(post=access_token_response)

    client = SpotifyClient(
        http_adapter=http_adapter,
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="REDIRECT_URI",
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
    assert auth_token == access_token_response
    assert client.auth_token == access_token_response


def test_me_successful():
    me_response = resource("responses/me.json")
    http_adapter = mock_http_adapter(get=me_response)

    client = SpotifyClient(auth_token=AUTH_TOKEN, http_adapter=http_adapter)
    profile = client.me()

    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {AUTH_TOKEN['access_token']}"},
    )

    assert profile == me_response


def test_me_requires_authorization():
    with pytest.raises(SpotifyNotAuthorized):
        SpotifyClient().me()


def test_me_when_token_expired():
    response = resource("responses/token_expired.json")
    http_adapter = mock_http_adapter(get=response)

    client = SpotifyClient(auth_token=AUTH_TOKEN, http_adapter=http_adapter)
    with pytest.raises(SpotifyWrongRequest):
        client.me()


def test_my_playlists():
    response = resource("responses/my_playlists.json")
    http_adapter = mock_http_adapter(get=response)
    client = SpotifyClient(auth_token=AUTH_TOKEN, http_adapter=http_adapter)
    playlists = client.my_playlists(limit=5, offset=10)
    http_adapter.get.assert_called_once_with(
        "https://api.spotify.com/v1/me/playlists",
        params={"limit": 5, "offset": 10},
        headers={"Authorization": f"Bearer {AUTH_TOKEN['access_token']}"},
    )
    assert playlists == response


def resource(filename: str) -> dict:
    with open(f"tests/gateways/resources/{filename}") as f:
        return json.load(f)


def mock_http_adapter(get=None, post=None) -> Mock:
    fake_http_adapter = Mock()
    if get is not None:
        fake_http_adapter.get.return_value = json_response(get)
    if post is not None:
        fake_http_adapter.post.return_value = json_response(post)
    return fake_http_adapter


def json_response(json: dict) -> Mock:
    fake_response = Mock()
    fake_response.json.return_value = json
    status_code = int(json["error"]["status"]) if "error" in json else 200
    fake_response.status_code = status_code
    return fake_response
