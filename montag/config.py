from pydantic import BaseSettings


class Configuration(BaseSettings):
    flask_secret_key: str = "<secret-key>"
    spotify_client_id: str = "<spotify-client-id>"
    spotify_client_secret: str = "<spotify-client-secret>"
    spotify_redirect_uri: str = "<spotify-redirect-uri>"


Config = Configuration()
