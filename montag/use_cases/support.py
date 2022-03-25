import functools
import logging
from typing import Optional

from montag.domain.entities import Playlist, PlaylistId
from montag.domain.errors import ApplicationError, NotFoundError
from montag.repositories.music_repo import MusicRepo
from montag.use_cases.types import Failure


def error_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApplicationError as e:
            return Failure(str(e))
        except Exception as e:
            logging.exception(e)
            return Failure(str(e))

    return wrapper


def fetch_mirror_playlist(
    src_playlist_id: PlaylistId, src_repo: MusicRepo, dst_repo: MusicRepo
) -> tuple[Playlist, Optional[Playlist]]:
    src_playlist = src_repo.find_playlist_by_id(src_playlist_id)
    if src_playlist:
        return (src_playlist, dst_repo.find_mirror_playlist(src_playlist))
    else:
        raise NotFoundError(f"Could not find a playlist with ID '{src_playlist_id}'.")
