from montag.clients.spotify import AuthToken
import secrets

from montag.domain import Playlist, Track


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
    return [track(**kwargs) for _ in range(qty)]


def playlist(name="The Playlist", is_liked=False):
    return Playlist(id=secrets.token_hex(5), name=name, is_liked=is_liked)
