from typing import Any, Callable, Tuple
from flask import g
from montag.system import System
from montag.use_cases.types import T, Response, Success


def system() -> System:
    if "system" not in g:
        g.system = System.build(
            spotify_auth_token=g.spotify_fetch_auth_token(),
            spotify_on_token_expired=g.spotify_on_token_expired,
        )
    return g.system


def as_json(response: Response[T], serializer: Callable[[Any], Any]) -> Tuple[dict, int]:
    if isinstance(response, Success):
        return {"data": serializer(response.value)}, 200
    else:
        return {"error": response.msg}, 500
