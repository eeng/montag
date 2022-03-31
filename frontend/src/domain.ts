enum Provider {
  SPOTIFY = "Spotify",
  YTMUSIC = "YouTubeMusic",
}

interface Playlist {
  id: string;
  name: string;
  is_liked: boolean;
}

export { Provider, Playlist };
