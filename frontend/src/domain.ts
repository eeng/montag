enum Provider {
  SPOTIFY = "Spotify",
  YTMUSIC = "YouTube Music",
}

interface Playlist {
  id: string;
  name: string;
  is_liked: boolean;
}

export { Provider, Playlist };
