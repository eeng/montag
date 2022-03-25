import json
from typing import Optional, Union
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


def mock_http_adapter(get=None, post=None, put=None, status_code=None) -> HttpAdapter:
    http_adapter = mock(HttpAdapter)
    if get is not None:
        http_adapter.get.return_value = fake_response(get, status_code)
    if post is not None:
        http_adapter.post.return_value = fake_response(post, status_code)
    if put is not None:
        http_adapter.put.return_value = fake_response(put, status_code)
    return http_adapter


# TODO i think there's a cleaner way with multiple dispatch
def fake_response(
    body=Union[dict, str], status_code: Optional[int] = None
) -> HttpResponse:
    response = mock(HttpResponse)
    if isinstance(body, dict):
        response.json.return_value = body
        # TODO this probably would not work with other non-Spotify response. Make tests pass the status
        response.status_code = status_code or (
            int(body["error"]["status"]) if "error" in body else 200
        )
        return response
    else:
        response.text = body
        response.json.side_effect = ValueError("Fake RequestsJSONDecodeError")
        response.status_code = status_code or 200
    return response


def fake_clock(timestamp: int) -> Clock:
    return mock(Clock, current_timestamp=timestamp)
