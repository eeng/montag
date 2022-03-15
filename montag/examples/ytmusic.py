from ytmusicapi import YTMusic

from montag.repositories.ytmusic import YouTubeMusicRepo


def client():
    return YTMusic("tmp/ytmusic_auth.json")


def repo():
    return YouTubeMusicRepo(client())
