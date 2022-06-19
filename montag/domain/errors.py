from montag.domain.entities import PlaylistId


class ApplicationError(Exception):
    """Base class for all application errors."""


class PlaylistNotFoundError(ApplicationError):
    """Raised when a playlist does not exists."""

    def __init__(self, playlist_id: PlaylistId) -> None:
        self.playlist_id = playlist_id
        super().__init__((f"Could not find a playlist with ID '{playlist_id}'"))
