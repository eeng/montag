import pytest
from montag.domain.entities import Provider
from montag.repositories.music_repo import MusicRepo
from montag.system import System
from montag.web.app import create_app
from montag.web.spotify_auth import AUTH_TOKEN_SESSION_KEY
from tests import factory
from tests.helpers import mock

# TODO repeated in test_spotify_auth
@pytest.fixture
def app():
    app = create_app()
    app.config.update(TESTING=True, SECRET_KEY="test_key")
    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_system(app):
    with app.app_context() as app_context:
        system = mock(System)
        app_context.g.system = system
        yield system


def test_me_when_not_authenticated_in_any_provider(client):
    response = client.get("/api/me")

    assert response.status_code == 200
    assert response.json == {"authorized_providers": []}


def test_me_when_authenticated_in_spotify(client):
    with client.session_transaction() as session:
        session[AUTH_TOKEN_SESSION_KEY] = factory.auth_token().dict()

    response = client.get("/api/me")

    assert response.status_code == 200
    assert response.json == {"authorized_providers": [Provider.SPOTIFY.value]}


# TODO maybe mock the use case somehow?
def test_playlists_success(client, mock_system):
    pl = factory.playlist()
    mock_system.repos = {Provider.SPOTIFY: mock(MusicRepo, find_playlists=[pl])}

    response = client.get("/api/playlists", query_string={"provider": "Spotify"})

    assert response.status_code == 200
    assert response.json == {"data": [pl.dict()]}


def test_playlists_error(client, mock_system):
    repo = mock(MusicRepo)
    repo.find_playlists.side_effect = ValueError("oops")
    mock_system.repos = {Provider.SPOTIFY: repo}

    response = client.get("/api/playlists", query_string={"provider": "Spotify"})

    assert response.status_code == 500
    assert response.json == {"error": "oops"}
