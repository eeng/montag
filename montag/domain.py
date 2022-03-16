from pydantic import BaseModel


class Track(BaseModel):
    name: str
    uri: str
    album: str
    artists: list[str]


class Playlist(BaseModel):
    id: str
    name: str
