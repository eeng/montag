from dataclasses import dataclass
from montag.gateways.spotify import SpotifyClient
from montag.models.track import Track


@dataclass
class SpotifyRepo:
    client: SpotifyClient

    def find_all_tracks(self) -> list[Track]:
        total = self.client.my_tracks(limit=1)["total"]
        limit = 50
        return [
            track
            for offset in range(0, total + 1, limit)
            for track in self.find_tracks(limit=limit, offset=offset)
        ]

    def find_tracks(self, **kargs) -> list[Track]:
        tracks_json = self.client.my_tracks(**kargs)
        return [
            Track(
                name=item["track"]["name"],
                uri=item["track"]["uri"],
                album=item["track"]["album"]["name"],
                artists=[artist["name"] for artist in item["track"]["artists"]],
            )
            for item in tracks_json["items"]
        ]
