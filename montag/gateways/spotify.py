import os
import secrets
from typing import Tuple
from urllib.parse import urlencode
from dataclasses import dataclass, field

BASE_URL = "https://accounts.spotify.com"
SCOPE = "user-read-private user-read-email"


@dataclass
class SpotifyClient:
    client_id: str = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret: str = os.environ["SPOTIFY_CLIENT_SECRET"]
    redirect_uri: str = os.environ["SPOTIFY_REDIRECT_URI"]

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


"""
Fiddles:
client = SpotifyClient()
client.authorize_url()
"""
