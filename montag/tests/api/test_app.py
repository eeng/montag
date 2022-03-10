import pytest
from montag.api.app import app
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
