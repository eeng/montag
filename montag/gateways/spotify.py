import os
import uuid
from urllib.parse import urlencode
from dataclasses import dataclass

BASE_URL = "https://accounts.spotify.com"
SCOPE = "user-read-private user-read-email"


@dataclass
class SpotifyClient:
    client_id: str = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret: str = os.environ["SPOTIFY_CLIENT_SECRET"]
    redirect_url: str = os.environ["SPOTIFY_REDIRECT_URL"]
    state: str = str(uuid.uuid4())

    def authorize_url(self):
        pass
        # params = dict(
        #     client_id=self.client_id,
        #     redirect_url=self.redirect_url,
        #     state=self.state,
        #     response_type="code",
        # )
        # return f"{BASE_URL}/authorize?{urlencode(params)}"


"""
Fiddles:
client = SpotifyClient()
"""
