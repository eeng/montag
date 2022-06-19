from dataclasses import dataclass

from montag.domain.entities import (
    Providers,
    Playlist,
    PlaylistId,
    Provider,
    Track,
    TrackId,
)
from montag.domain.errors import PlaylistNotFoundError
from montag.repositories.music_repo import MusicRepo
from ytmusicapi import YTMusic

LIKED_MUSIC_PLAYLIST_ID = Providers[Provider.YT_MUSIC].liked_songs_playlist


@dataclass
class YouTubeMusicRepo(MusicRepo):
    client: YTMusic

    def find_playlists(self) -> list[Playlist]:
        response = self.client.get_library_playlists()
        return [
            Playlist(
                id=item["playlistId"],
                name=item["title"],
                is_liked=item["playlistId"] == LIKED_MUSIC_PLAYLIST_ID,
            )
            for item in response
        ]

    def find_tracks(self, playlist_id: PlaylistId) -> list[Track]:
        try:
            response = self.client.get_playlist(playlistId=playlist_id)
            return self._track_from_json(response["tracks"])
        except Exception as e:
            if "404" in str(e):
                raise PlaylistNotFoundError(playlist_id)
            else:
                raise e

    def search_matching_tracks(self, target: Track, limit=10) -> list[Track]:
        q = f"{target.name} {target.artists[0]}"
        response = self.client.search(q, filter="songs", limit=limit)
        # Slicing here since YTMusic seems to ignore the limit param
        return self._track_from_json(response[0:limit])

    def _track_from_json(self, tracks_json: list[dict]):
        return [
            Track(
                id=item["videoId"],
                name=item["title"],
                album=(item.get("album") and item["album"]["name"]),
                artists=[artist["name"] for artist in item["artists"]],
            )
            for item in tracks_json
        ]

    def create_playlist(self, name: str) -> Playlist:
        response = self.client.create_playlist(name, description="")
        if isinstance(response, str):
            playlist = self.find_playlist_by_id(response)
            if not playlist:
                raise YTMusicError("Created playlist not found? This is unexpected")
            return playlist
        else:
            raise YTMusicError(response)

    def add_tracks(self, playlist_id: PlaylistId, track_ids: list[TrackId]) -> None:
        if playlist_id == LIKED_MUSIC_PLAYLIST_ID:
            for track_id in track_ids:
                self.client.rate_song(track_id, "LIKE")
        else:
            response = self.client.add_playlist_items(playlist_id, track_ids)
            if isinstance(response, dict) and "SUCCEEDED" in response["status"]:
                pass
            else:
                raise YTMusicError(response)


class YTMusicError(Exception):
    """Used for all YTMusic library errors."""
