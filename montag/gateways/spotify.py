import os
import secrets
from urllib.parse import urlencode
from dataclasses import dataclass, field

BASE_URL = "https://accounts.spotify.com"
SCOPE = "user-read-private user-read-email"


@dataclass
class SpotifyClient:
    client_id: str = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret: str = os.environ["SPOTIFY_CLIENT_SECRET"]
    redirect_uri: str = os.environ["SPOTIFY_REDIRECT_URI"]
    state: str = field(default_factory=lambda: str(secrets.token_hex(8)))

    def authorize_url(self):
        params = dict(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=self.state,
            scope=SCOPE,
            response_type="code",
        )
        return f"{BASE_URL}/authorize?{urlencode(params)}"


"""
Fiddles:
client = SpotifyClient()
client.authorize_url()
"""
