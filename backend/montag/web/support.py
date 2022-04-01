from functools import singledispatch
from typing import Any, Callable, Tuple

from flask import g
from montag.system import System
from montag.use_cases.types import Failure, Response, Success, T


def system() -> System:
    if "system" not in g:
        g.system = System.build(
            spotify_auth_token=g.spotify_fetch_auth_token(),
            spotify_on_token_expired=g.spotify_on_token_expired,
        )
    return g.system


Serializer = Callable[[Any], Any]
identity = lambda v: v


@singledispatch
def as_json(response: Any, serializer: Serializer = identity) -> Tuple[dict, int]:
    raise NotImplementedError


@as_json.register(Success)
def _(response: Success, serializer: Serializer = identity) -> Tuple[dict, int]:
    return {"data": serializer(response.value)}, 200


@as_json.register(Failure)
def _(response: Failure, serializer: Serializer = identity) -> Tuple[dict, int]:
    return {"error": response.msg}, 500


@as_json.register(dict)
def _(response: dict, serializer: Serializer = identity) -> Tuple[dict, int]:
    return {"data": serializer(response)}, 200
