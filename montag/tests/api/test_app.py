import pytest
from montag.api.app import SPOTIFY_STATE_KEY, app
from montag.gateways import spotify


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_spotify_login(client):
    response = client.get("/spotify/login")
    assert response.status_code == 302
    assert spotify.BASE_URL in response.headers["Location"]
    assert "spotify_auth_state" in response.headers["Set-Cookie"]


def test_spotify_callback_with_matching_state(client):
    client.set_cookie("localhost", SPOTIFY_STATE_KEY, "the-state")
    response = client.get("/spotify/callback", query_string={"state": "the-state"})
    assert response.status_code == 200


def test_spotify_callback_with_wrong_state(client):
    client.set_cookie("localhost", SPOTIFY_STATE_KEY, "sent-state")
    response = client.get("/spotify/callback", query_string={"state": "received-state"})
    assert response.status_code == 403
