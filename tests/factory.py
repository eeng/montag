from montag.clients.spotify_client import AuthToken
import secrets

from montag.domain.entities import Playlist, Track


def auth_token(expires_at=None):
    return AuthToken(
        access_token=secrets.token_hex(3),
        refresh_token=secrets.token_hex(3),
        expires_at=expires_at or 9647168435,
    )


def track(name="The Name", album="The Album", artists=["The Artist"]):
    return Track(
        id=secrets.token_hex(5),
        name=name,
        album=album,
        artists=artists,
    )


def tracks(qty: int, **kwargs) -> list[Track]:
    return repeat(qty, track, **kwargs)


def playlist(name="The Playlist", is_liked=False):
    return Playlist(id=secrets.token_hex(5), name=name, is_liked=is_liked)


def playlists(qty: int, **kwargs) -> list[Playlist]:
    return repeat(qty, playlist, **kwargs)


def repeat(times, fun, **kwargs):
    return [fun(**kwargs) for _ in range(times)]
