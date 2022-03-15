import os
import secrets
from dataclasses import dataclass
from typing import Callable, Optional
from urllib.parse import urlencode
from pydantic import BaseModel
from montag.repositories.spotify import SpotifyClient as SpotifyClientProtocol
from montag.gateways.http import HttpAdapter, HttpResponse
from montag.util.clock import Clock

ACCOUNTS_URL = "https://accounts.spotify.com"
API_URL = "https://api.spotify.com/v1"
SCOPE = "user-read-private user-read-email user-library-read playlist-read-private"


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int


@dataclass
class SpotifyClient(SpotifyClientProtocol):
    client_id: str = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret: str = os.environ["SPOTIFY_CLIENT_SECRET"]
    redirect_uri: str = os.environ["SPOTIFY_REDIRECT_URI"]
    auth_token: Optional[AuthToken] = None
    on_token_expired: Callable[[AuthToken], None] = lambda _: None
    http_adapter: HttpAdapter = HttpAdapter()
    clock: Clock = Clock()

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

    def request_access_token(self, code: str) -> AuthToken:
        data = dict(
            grant_type="authorization_code",
            code=code,
            redirect_uri=self.redirect_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        response = self.http_adapter.post(f"{ACCOUNTS_URL}/api/token", data=data)
        json = self._parse_response(response)
        self.auth_token = self._extract_auth_token(json, json)
        return self.auth_token

    def refresh_access_token(self) -> AuthToken:
        if self.auth_token is None:
            raise NotAuthorizedError

        data = dict(
            grant_type="refresh_token",
            refresh_token=self.auth_token.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        response = self.http_adapter.post(f"{ACCOUNTS_URL}/api/token", data=data)
        json = self._parse_response(response)
        self.auth_token = self._extract_auth_token(json, self.auth_token.dict())
        return self.auth_token

    def _extract_auth_token(self, json, refresh_token_dict) -> AuthToken:
        return AuthToken(
            refresh_token=refresh_token_dict["refresh_token"],
            access_token=json["access_token"],
            expires_at=self.clock.current_timestamp() + json["expires_in"],
        )

    def refresh_access_token_if_needed(self) -> Optional[AuthToken]:
        if self.auth_token is None:
            raise NotAuthorizedError
        if self.clock.current_timestamp() >= self.auth_token.expires_at:
            new_auth_token = self.refresh_access_token()
            self.on_token_expired(new_auth_token)
            return new_auth_token
        return None

    def me(self):
        self.refresh_access_token_if_needed()
        response = self.http_adapter.get(f"{API_URL}/me", headers=self._auth_header())
        return self._parse_response(response)

    def my_playlists(self, limit: int = 50, offset: int = 0):
        self.refresh_access_token_if_needed()
        response = self.http_adapter.get(
            f"{API_URL}/me/playlists",
            params=dict(limit=limit, offset=offset),
            headers=self._auth_header(),
        )
        return self._parse_response(response)

    def liked_tracks(self, limit: int = 50, offset: int = 0):
        self.refresh_access_token_if_needed()
        response = self.http_adapter.get(
            f"{API_URL}/me/tracks",
            params=dict(limit=limit, offset=offset),
            headers=self._auth_header(),
        )
        return self._parse_response(response)

    def playlist_tracks(self, playlist_id: str, limit: int = 50, offset: int = 0):
        self.refresh_access_token_if_needed()
        response = self.http_adapter.get(
            f"{API_URL}/playlists/{playlist_id}/tracks",
            params=dict(limit=limit, offset=offset),
            headers=self._auth_header(),
        )
        return self._parse_response(response)

    def _auth_header(self):
        if self.auth_token is None:
            raise NotAuthorizedError

        bearer = self.auth_token.access_token
        return {"Authorization": f"Bearer {bearer}"}

    def _parse_response(self, response: HttpResponse):
        json = response.json()
        if response.status_code == 200:
            return json
        else:
            raise BadRequestError(json)


class SpotifyError(Exception):
    """Base class for all Spotify errors"""


class BadRequestError(SpotifyError):
    """Raised when the API replies with a non-200 status code."""


class NotAuthorizedError(SpotifyError):
    """Raised when the authorization flow hasn't been started yet."""


class BadStateError(SpotifyError):
    """Raised when the authorization flow sent state doesn't match the received one."""
