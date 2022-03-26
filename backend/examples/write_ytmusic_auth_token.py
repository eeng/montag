from ytmusicapi import YTMusic

YTMusic.setup(filepath="tmp/ytmusic_auth.json")

# Usage:
# 1. Copy the headers as indicated in: https://ytmusicapi.readthedocs.io/en/latest/setup.html#authenticated-requests
# 2. At the terminal run:
# pbpaste | poetry run python examples/write_ytmusic_auth_token.py
