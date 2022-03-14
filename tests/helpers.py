import json
from unittest.mock import Mock
from callee import Matcher
from montag.gateways.http import HttpAdapter, HttpResponse
from montag.util.clock import Clock


def resource(filename: str) -> dict:
    with open(f"tests/resources/{filename}") as f:
        return json.load(f)


def mock_http_adapter(get=None, post=None) -> HttpAdapter:
    http_adapter = Mock()
    if get is not None:
        http_adapter.get.return_value = fake_json_response(get)
    if post is not None:
        http_adapter.post.return_value = fake_json_response(post)
    return http_adapter


def fake_json_response(json: dict) -> HttpResponse:
    response = Mock()
    response.json.return_value = json
    status_code = int(json["error"]["status"]) if "error" in json else 200
    response.status_code = status_code
    return response


def fake_clock(timestamp: int) -> Clock:
    clock = Mock()
    clock.current_timestamp.return_value = timestamp
    return clock


class HasEntry(Matcher):
    """Matches a dict contains the specified key/value entry."""

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def match(self, a_dict):
        return a_dict.get(self.key) == self.value
