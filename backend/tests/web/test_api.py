import pytest
from flask.testing import FlaskClient
from montag.domain.entities import Provider
from montag.web.app import create_app
from montag.web.spotify_auth import AUTH_TOKEN_SESSION_KEY
from tests import factory


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY="test_key")
    with app.test_client() as client:
        yield client


def test_me_when_not_authenticated_in_any_provider(client: FlaskClient):
    response = client.get("/api/me")

    assert response.status_code == 200
    assert response.json == {"authorized_providers": []}


def test_me_when_authenticated_in_spotify(client: FlaskClient):
    with client.session_transaction() as session:
        session[AUTH_TOKEN_SESSION_KEY] = factory.auth_token().dict()

    response = client.get("/api/me")

    assert response.status_code == 200
    assert response.json == {"authorized_providers": [Provider.SPOTIFY.value]}
