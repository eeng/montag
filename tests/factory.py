from montag.clients.spotify import AuthToken
import secrets

from montag.domain import Track


def auth_token(expires_at=None):
    return AuthToken(
        access_token=secrets.token_hex(3),
        refresh_token="AQAXsR",
        expires_at=expires_at or 9647168435,
    )


def track(name="The Name", album="The Album", artist="The Artist"):
    return Track(
        id=secrets.token_hex(5),
        name=name,
        album=album,
        artists=[artist],
    )
