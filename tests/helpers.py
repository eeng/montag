import json
from typing import Optional
from unittest.mock import Mock, create_autospec

from montag.clients.http import HttpAdapter, HttpResponse
from montag.util.clock import Clock


def resource(filename: str) -> dict:
    with open(f"tests/resources/{filename}") as f:
        return json.load(f)


def mock(cls, **methods_to_stub) -> Mock:
    """Allows to create a mock and stub its methods in one line."""
    m = create_autospec(cls)
    for (method, return_value) in methods_to_stub.items():
        getattr(m, method).return_value = return_value
    return m


def mock_http_adapter(get=None, post=None, status_code=None) -> HttpAdapter:
    http_adapter = mock(HttpAdapter)
    if get is not None:
        http_adapter.get.return_value = fake_json_response(get, status_code)
    if post is not None:
        http_adapter.post.return_value = fake_json_response(post, status_code)
    return http_adapter


def fake_json_response(json: dict, status_code: Optional[int] = None) -> HttpResponse:
    response = mock(HttpResponse, json=json)
    response.status_code = status_code or (
        int(json["error"]["status"]) if "error" in json else 200
    )
    return response


def fake_clock(timestamp: int) -> Clock:
    return mock(Clock, current_timestamp=timestamp)
