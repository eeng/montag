from montag.domain.entities import Provider
from montag.use_cases.types import Failure, Success, UseCase
from montag.web.spotify_auth import AUTH_TOKEN_SESSION_KEY
from tests import factory
from tests.helpers import mock


def test_me_when_not_authenticated_in_any_provider(client):
    response = client.get("/api/me")

    assert response.status_code == 200
    assert response.json == {"data": {"authorized_providers": []}}


def test_me_when_authenticated_in_spotify(client):
    with client.session_transaction() as session:
        session[AUTH_TOKEN_SESSION_KEY] = factory.auth_token().dict()

    response = client.get("/api/me")

    assert response.status_code == 200
    assert response.json == {"data": {"authorized_providers": [Provider.SPOTIFY.value]}}


def test_playlists_success(client, mock_system):
    pl = factory.playlist()
    mock_system.fetch_playlists_use_case = mock(UseCase, execute=Success([pl]))

    response = client.get("/api/playlists", query_string={"provider": "Spotify"})

    assert response.status_code == 200
    assert response.json == {"data": [pl.dict()]}


def test_playlists_error(client, mock_system):
    mock_system.fetch_playlists_use_case = mock(UseCase, execute=Failure("oops"))

    response = client.get("/api/playlists", query_string={"provider": "Spotify"})

    assert response.status_code == 500
    assert response.json == {"error": "oops"}
