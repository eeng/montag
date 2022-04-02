from flask import session
from montag.web.ytmusic_auth import AUTH_TOKEN_SESSION_KEY
from tests.helpers import resource


def test_ytmusic_login(client):
    return_to = "http://some-domain"
    response = client.post(
        "/ytmusic/login",
        data={"headers_raw": resource("ytmusic/headers_raw"), "return_to": return_to},
    )

    assert response.status_code == 302
    assert AUTH_TOKEN_SESSION_KEY in session
    assert return_to in response.headers["Location"]
