from montag.repositories.ytmusic import YouTubeMusicClient
from ytmusicapi import YTMusic


class YTMusicAdapter(YouTubeMusicClient):
    def __init__(self, auth: str) -> None:
        self.yt_music = YTMusic(auth)

    def my_playlists(self) -> list[dict]:
        return self.yt_music.get_library_playlists()
