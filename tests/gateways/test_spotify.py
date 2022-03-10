from montag.gateways.spotify import SpotifyClient


def test_authorize_url():
    actual_url, state = SpotifyClient(
        client_id="FAKE_CLIENT_ID",
        client_secret="FAKE_CLIENT_SECRET",
        redirect_uri="FAKE_REDIRECT_URL",
    ).authorize_url_and_state()

    expected_url = (
        "https://accounts.spotify.com/authorize?"
        "client_id=FAKE_CLIENT_ID&"
        "redirect_uri=FAKE_REDIRECT_URL&"
        f"state={state}&"
        "scope=user-read-private+user-read-email&"
        "response_type=code"
    )
    assert actual_url == expected_url


def test_state_changes_with_every_call():
    client = SpotifyClient()
    _, state1 = client.authorize_url_and_state()
    _, state2 = client.authorize_url_and_state()
    assert state1 != state2
