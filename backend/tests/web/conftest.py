import pytest
from montag.system import System
from montag.web.app import create_app
from tests.helpers import mock


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
