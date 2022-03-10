from unittest.mock import Mock
from montag.gateways.spotify import SpotifyClient
import json


def authorize_url_and_state():
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
    access_token_response = resource("access_token_response.json")

    fake_http_adapter = Mock()
    fake_http_adapter.post.return_value = json_response(access_token_response)

    client = SpotifyClient(
        http_adapter=fake_http_adapter,
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="REDIRECT_URI",
    )
    token = client.request_access_token("SOME_CODE")

    fake_http_adapter.post.assert_called_once_with(
        "https://accounts.spotify.com/api/token",
        data=dict(
            grant_type="authorization_code",
            code="SOME_CODE",
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
            redirect_uri="REDIRECT_URI",
        ),
    )
    assert token == access_token_response


def resource(filename: str) -> dict:
    with open(f"tests/gateways/resources/{filename}") as f:
        return json.load(f)


def json_response(json: dict) -> Mock:
    fake_response = Mock()
    fake_response.json.return_value = json
    return fake_response
