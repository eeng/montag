import os
import secrets
import requests
from dataclasses import dataclass
from types import ModuleType
from typing import Tuple
from urllib.parse import urlencode

BASE_URL = "https://accounts.spotify.com"
SCOPE = "user-read-private user-read-email"


@dataclass
class SpotifyClient:
    client_id: str = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret: str = os.environ["SPOTIFY_CLIENT_SECRET"]
    redirect_uri: str = os.environ["SPOTIFY_REDIRECT_URI"]
    http_adapter: ModuleType = requests

    def authorize_url_and_state(self) -> Tuple[str, str]:
        state = secrets.token_hex(8)
        params = dict(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=state,
            scope=SCOPE,
            response_type="code",
        )
        return (f"{BASE_URL}/authorize?{urlencode(params)}", state)

    def request_access_token(self, code):
        data = dict(
            grant_type="authorization_code",
            code=code,
            redirect_uri=self.redirect_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        response = self.http_adapter.post(f"{BASE_URL}/api/token", data=data)
        return response.json()

    def request_refreshed_token(self, refresh_token):
        data = dict(
            grant_type="refresh_token",
            refresh_token=refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        response = self.http_adapter.post(f"{BASE_URL}/api/token", data=data)
        return response.json()


"""
    client = SpotifyClient()
    url, _ = client.authorize_url_and_state()
    code = input(f"Go to {url} and then paste code here: ")
    token = client.request_access_token(code)
    print(f"Token: {token}")
"""
