import os
import secrets
import requests
from dataclasses import dataclass
from types import ModuleType
from typing import Optional, TypedDict
from urllib.parse import urlencode

ACCOUNTS_URL = "https://accounts.spotify.com"
API_URL = "https://api.spotify.com/v1"
SCOPE = "user-read-private user-read-email"


class AuthToken(TypedDict):
    access_token: str
    refresh_token: str


@dataclass
class SpotifyClient:
    client_id: str = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret: str = os.environ["SPOTIFY_CLIENT_SECRET"]
    redirect_uri: str = os.environ["SPOTIFY_REDIRECT_URI"]
    http_adapter: ModuleType = requests
    auth_token: Optional[AuthToken] = None

    def authorize_url_and_state(self) -> tuple[str, str]:
        state = secrets.token_hex(8)
        params = dict(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=state,
            scope=SCOPE,
            response_type="code",
        )
        return (f"{ACCOUNTS_URL}/authorize?{urlencode(params)}", state)

    def request_access_token(self, code):
        data = dict(
            grant_type="authorization_code",
            code=code,
            redirect_uri=self.redirect_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        response = self.http_adapter.post(f"{ACCOUNTS_URL}/api/token", data=data)
        self.auth_token = response.json()
        return self.auth_token

    def request_refreshed_token(self):
        data = dict(
            grant_type="refresh_token",
            refresh_token=self.auth_token["refresh_token"],
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        response = self.http_adapter.post(f"{ACCOUNTS_URL}/api/token", data=data)
        return response.json()

    def me(self):
        response = self.http_adapter.get(f"{API_URL}/me", headers=self._auth_header())
        return self._parse_response(response)

    def my_playlists(self, limit=50, offset=0):
        response = self.http_adapter.get(
            f"{API_URL}/me/playlists",
            params=dict(limit=limit, offset=offset),
            headers=self._auth_header(),
        )
        return self._parse_response(response)

    def _auth_header(self):
        if self.auth_token is None:
            raise SpotifyNotAuthorized

        bearer = self.auth_token["access_token"]
        return {"Authorization": f"Bearer {bearer}"}

    def _parse_response(self, response):
        json = response.json()
        if response.status_code == 200:
            return json
        else:
            raise SpotifyWrongRequest(json)


class SpotifyWrongRequest(Exception):
    """Raised when the API replies with a non-200 status code."""

    pass


class SpotifyNotAuthorized(Exception):
    """Raised when the authorization flow hasn't been started yet."""

    pass


"""
client = SpotifyClient()
url, _ = client.authorize_url_and_state()
code = input(f"Go to {url} and then paste code here: ")
auth_token = client.request_access_token(code)
"""
