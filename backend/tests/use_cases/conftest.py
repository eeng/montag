import pytest
from montag.domain.entities import Provider
from montag.repositories.music_repo import MusicRepo
from tests.helpers import mock


@pytest.fixture
def spotify_repo():
    return mock(MusicRepo)


@pytest.fixture
def ytmusic_repo():
    return mock(MusicRepo)


@pytest.fixture
def repos(spotify_repo, ytmusic_repo) -> dict[Provider, MusicRepo]:
    return {
        Provider.SPOTIFY: spotify_repo,
        Provider.YT_MUSIC: ytmusic_repo,
    }
