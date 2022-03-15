from montag.clients.spotify import AuthToken
import secrets


def auth_token(expires_at=None):
    return AuthToken(
        access_token=secrets.token_hex(3),
        refresh_token="AQAXsR",
        expires_at=expires_at or 9647168435,
    )
