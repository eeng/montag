from ytmusicapi import YTMusic

if __name__ == "__main__":
    YTMusic.setup(filepath="tmp/yt_music_auth_headers.json")

# MacOS terminal doesn't allow to paste big lines, so in order to do the YTMusic.setup,
# copy the headers to the clipboard and then use pbpaste, like so:
# pbpaste | poetry run python montag/examples/youtube_music.py
