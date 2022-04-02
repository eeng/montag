import pytest
from flask import session
from montag.clients.spotify_client import ACCOUNTS_URL, SpotifyClient
from montag.web.spotify_auth import AUTH_STATE_SESSION_KEY, AUTH_TOKEN_SESSION_KEY
from tests import factory
from tests.helpers import mock


@pytest.fixture
def mock_spotify_client(mock_system):
    client = mock(SpotifyClient)
    mock_system.spotify_client = client
    yield client


def test_spotify_login(client):
    response = client.get("/spotify/login", query_string={"return_to": "..."})
    assert response.status_code == 302
    assert ACCOUNTS_URL in response.headers["Location"]
    assert AUTH_STATE_SESSION_KEY in session


def test_spotify_callback_with_matching_state(client, mock_spotify_client):
    code = "SOME_CODE"
    state = "SOME_STATE"
    return_to = "..."
    token = factory.auth_token()

    with client.session_transaction() as session:
        session[AUTH_STATE_SESSION_KEY] = (state, return_to)
    mock_spotify_client.request_access_token.return_value = token

    query_string = {"state": state, "code": code}
    response = client.get("/spotify/callback", query_string=query_string)

    mock_spotify_client.request_access_token.assert_called_once_with(code)
    with client.session_transaction() as session:
        assert session[AUTH_TOKEN_SESSION_KEY] == token
    assert response.status_code == 302


def test_spotify_callback_with_wrong_state(client):
    with client.session_transaction() as session:
        session[AUTH_STATE_SESSION_KEY] = ("sent_state", "<return_to>")
    with pytest.raises(ValueError):
        client.get("/spotify/callback", query_string={"state": "received-state"})
