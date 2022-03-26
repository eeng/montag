from dataclasses import dataclass
from typing import Callable, Optional
from urllib.parse import urlencode

from montag.clients.http import HttpAdapter, HttpResponse
from montag.config import Config
from montag.util.clock import Clock
from pydantic import BaseModel

ACCOUNTS_URL = "https://accounts.spotify.com"
API_URL = "https://api.spotify.com/v1"
SCOPES = [
    "user-read-private",
    "user-read-email",
    "user-library-read",
    "user-library-modify",
    "playlist-read-private",
    "playlist-modify-private",
]


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int


@dataclass
class SpotifyClient:
    client_id: str = Config.spotify_client_id
    client_secret: str = Config.spotify_client_secret
    redirect_uri: str = Config.spotify_redirect_uri
    auth_token: Optional[AuthToken] = None
    on_token_expired: Callable[[AuthToken], None] = lambda _: None
    http_adapter: HttpAdapter = HttpAdapter()
    clock: Clock = Clock()

    def authorize_url(self, state: str = "") -> str:
        params = dict(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=state,
            scope=" ".join(SCOPES),
            response_type="code",
        )
        return f"{ACCOUNTS_URL}/authorize?{urlencode(params)}"

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

    def me(self) -> dict:
        return self._authorized_api_get("/me")

    def my_playlists(self, limit: int = 20, offset: int = 0) -> dict:
        return self._authorized_api_get("/me/playlists", limit=limit, offset=offset)

    def liked_tracks(self, limit: int = 20, offset: int = 0) -> dict:
        return self._authorized_api_get("/me/tracks", limit=limit, offset=offset)

    def playlist_tracks(self, playlist_id: str, limit: int = 20, offset: int = 0) -> dict:
        return self._authorized_api_get(f"/playlists/{playlist_id}/tracks", limit=limit, offset=offset)

    def add_liked_tracks(self, track_ids: list[str]) -> None:
        self._authorized_api_put("/me/tracks", ids=track_ids)

    def add_playlist_tracks(self, playlist_id: str, track_ids: list[str]) -> None:
        track_uris = [f"spotify:track:{id}" for id in track_ids]
        self._authorized_api_post(f"/playlists/{playlist_id}/tracks", uris=track_uris)

    def search(self, query: str, type: str, limit: int = 20, offset: int = 0) -> dict:
        return self._authorized_api_get("/search", q=query, type=type, limit=limit, offset=offset)

    def create_playlist(self, name: str) -> dict:
        return self._authorized_api_post("/me/playlists", name=name, public=False)

    def _authorized_api_get(self, path: str, **params):
        self.refresh_access_token_if_needed()
        response = self.http_adapter.get(
            API_URL + path,
            params=params,
            headers=self._auth_header(),
        )
        return self._parse_response(response)

    def _authorized_api_post(self, path: str, **json):
        self.refresh_access_token_if_needed()
        response = self.http_adapter.post(
            API_URL + path,
            json=json,
            headers=self._auth_header(),
        )
        return self._parse_response(response)

    def _authorized_api_put(self, path: str, **json):
        self.refresh_access_token_if_needed()
        response = self.http_adapter.put(
            API_URL + path,
            json=json,
            headers=self._auth_header(),
        )
        return self._parse_response(response, decode_json_on_success=False)

    def _auth_header(self):
        if self.auth_token is None:
            raise NotAuthorizedError

        bearer = self.auth_token.access_token
        return {"Authorization": f"Bearer {bearer}"}

    def _parse_response(self, response: HttpResponse, decode_json_on_success=True):
        if 200 <= response.status_code <= 299:
            return response.json() if decode_json_on_success else {}
        else:
            raise BadRequestError(response.json())


class SpotifyError(Exception):
    """Base class for all Spotify errors"""


class BadRequestError(SpotifyError):
    """Raised when the API replies with a non-200 status code."""


class NotAuthorizedError(SpotifyError):
    """Raised when the authorization flow hasn't been started yet."""


# TODO doesn't belong here
class BadStateError(SpotifyError):
    """Raised when the authorization flow sent state doesn't match the received one."""
