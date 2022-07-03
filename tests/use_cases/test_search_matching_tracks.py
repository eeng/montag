from tokenize import Pointfloat
from unittest.mock import call

from montag.domain.entities import Provider, SuggestedTrack, Track
from montag.domain.errors import PlaylistNotFoundError
from montag.use_cases.search_matching_tracks import SearchMatchingTracks, TrackSuggestions
from montag.use_cases.support import Failure, Success
from tests import factory


def test_search_tracks_matching_the_ones_in_the_src_playlist(repos, spotify_repo, ytmusic_repo):
    src_playlist_id = "PLVUD"
    dst_playlist_id = "WERQZ"
    track1, track2 = factory.track(name="T1"), factory.track(name="T2")
    track1_suggestions = factory.tracks(2, name="For T1")
    track2_suggestions = factory.tracks(3, name="For T2")

    spotify_repo.find_tracks.return_value = [track1, track2]
    ytmusic_repo.find_tracks.return_value = []
    ytmusic_repo.search_matching_tracks.side_effect = [
        track1_suggestions,
        track2_suggestions,
    ]

    request = SearchMatchingTracks.Request(
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
        src_playlist_id=src_playlist_id,
        dst_playlist_id=dst_playlist_id,
    )
    response = SearchMatchingTracks(repos).execute(request)

    assert response == Success(
        [
            TrackSuggestions(
                target=track1, suggestions=list(map(SuggestedTrack.build, track1_suggestions))
            ),
            TrackSuggestions(
                target=track2, suggestions=list(map(SuggestedTrack.build, track2_suggestions))
            ),
        ]
    )
    spotify_repo.find_tracks.assert_called_once_with(src_playlist_id)
    ytmusic_repo.find_tracks.assert_called_once_with(dst_playlist_id)
    ytmusic_repo.search_matching_tracks.assert_has_calls(
        [call(track1, limit=5), call(track2, limit=5)]
    )


def test_when_a_track_already_exists_in_dst_playlist(repos, spotify_repo, ytmusic_repo):
    spotify_playlist = factory.playlist(name="Classics")
    ytmusic_playlist = factory.playlist(name="Classics")

    src_track = factory.track(name="T1")
    dst_t1, dst_t2, dst_t3 = [
        factory.track(name="S1"),
        factory.track(name="S2"),
        factory.track(name="S3"),
    ]

    spotify_repo.find_tracks.return_value = [src_track]
    ytmusic_repo.find_tracks.return_value = [dst_t1, dst_t3]
    ytmusic_repo.search_matching_tracks.return_value = [dst_t1, dst_t2]

    request = SearchMatchingTracks.Request(
        src_provider=Provider.SPOTIFY,
        src_playlist_id=spotify_playlist.id,
        dst_provider=Provider.YT_MUSIC,
        dst_playlist_id=ytmusic_playlist.id,
    )
    response = SearchMatchingTracks(repos).execute(request)

    assert response == Success(
        [
            TrackSuggestions(
                target=src_track,
                suggestions=[
                    SuggestedTrack(**dst_t1.dict(), already_present=True),
                    SuggestedTrack(**dst_t2.dict(), already_present=False),
                ],
            )
        ]
    )
    ytmusic_repo.find_tracks.assert_called_once_with(ytmusic_playlist.id)


def test_when_src_playlist_do_not_exists(repos, spotify_repo):
    error = PlaylistNotFoundError("WQRSD", Provider.YT_MUSIC)
    spotify_repo.find_tracks.side_effect = error
    request = SearchMatchingTracks.Request(
        src_playlist_id="inexistent",
        dst_playlist_id="inexistent",
        src_provider=Provider.SPOTIFY,
        dst_provider=Provider.YT_MUSIC,
    )

    response = SearchMatchingTracks(repos).execute(request)

    assert response == Failure(
        "Could not find a playlist with ID 'WQRSD' in Provider.YT_MUSIC", error
    )
