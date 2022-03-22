from dataclasses import dataclass
from montag.domain import Playlist
from montag.repositories.music_repo import MusicRepo
from tests import factory


@dataclass
class FakeRepo(MusicRepo):  # type: ignore
    playlists: list[Playlist]

    def find_playlists(self) -> list[Playlist]:
        return self.playlists


def test_find_mirror_playlist():
    your_likes, classics, nineties_rock = dst_playlists = [
        factory.playlist(name="Your Likes", is_liked=True),
        factory.playlist(name="Classics"),
        factory.playlist(name="90s Rock"),
    ]

    def do_find(src_playlist):
        return FakeRepo(dst_playlists).find_mirror_playlist(src_playlist)

    assert do_find(factory.playlist(name="Liked Songs", is_liked=True)) == your_likes
    assert do_find(factory.playlist(name="Classics")) == classics
    assert do_find(factory.playlist(name="90s Rock")) == nineties_rock
    assert do_find(factory.playlist(name="Other")) == None
