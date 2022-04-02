enum Provider {
  SPOTIFY = "spotify",
  YT_MUSIC = "ytmusic",
}

interface Playlist {
  id: string;
  name: string;
  is_liked: boolean;
}

export { Provider, Playlist };
