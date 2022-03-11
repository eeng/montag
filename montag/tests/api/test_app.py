import pytest
from unittest.mock import Mock
from flask import session
from montag.api.app import SPOTIFY_COOKIE_KEY, SPOTIFY_SESSION_KEY, app
from montag.gateways import spotify


def test_spotify_login(client):
    response = client.get("/spotify/login")
    assert response.status_code == 302
    assert spotify.ACCOUNTS_URL in response.headers["Location"]
    assert "spotify_auth_state" in response.headers["Set-Cookie"]


def test_spotify_callback_with_matching_state(client, mock_spotify_client):
    code = "SOME_CODE"
    state = "SOME_STATE"
    token = {"access_token": "SOME_ACCESS_TOKEN"}

    client.set_cookie("localhost", SPOTIFY_COOKIE_KEY, state)
    mock_spotify_client.request_access_token.return_value = token

    query_string = {"state": state, "code": code}
    response = client.get("/spotify/callback", query_string=query_string)

    mock_spotify_client.request_access_token.assert_called_once_with(code)
    assert session[SPOTIFY_SESSION_KEY] == token
    assert response.status_code == 200


def test_spotify_callback_with_wrong_state(client, mock_spotify_client):
    client.set_cookie("localhost", SPOTIFY_COOKIE_KEY, "sent-state")
    response = client.get("/spotify/callback", query_string={"state": "received-state"})
    mock_spotify_client.request_access_token.assert_not_called()
    assert response.status_code == 403


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_key"
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_spotify_client():
    with app.app_context() as app_context:
        mock = Mock()
        app_context.g.spotify_client = mock
        yield mock
