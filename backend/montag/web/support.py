from flask import g
from montag.system import System


def system() -> System:
    if "system" not in g:
        g.system = System.build(
            spotify_auth_token=g.spotify_fetch_auth_token(),
            spotify_on_token_expired=g.spotify_on_token_expired,
        )
    return g.system
