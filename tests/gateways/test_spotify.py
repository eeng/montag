from montag.gateways.spotify import SpotifyClient


def test_authorize_url():
    client = SpotifyClient(
        client_id="FAKE_CLIENT_ID",
        client_secret="FAKE_CLIENT_SECRET",
        redirect_uri="FAKE_REDIRECT_URL",
        state="FAKE_STATE",
    )
    expected_url = (
        "https://accounts.spotify.com/authorize?"
        "client_id=FAKE_CLIENT_ID&"
        "redirect_uri=FAKE_REDIRECT_URL&"
        "state=FAKE_STATE&"
        "scope=user-read-private+user-read-email&"
        "response_type=code"
    )
    assert client.authorize_url() == expected_url


def test_state_is_different_on_every_instance():
    client1 = SpotifyClient()
    client2 = SpotifyClient()
    assert client1.state != client2.state
