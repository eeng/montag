enum Provider {
  SPOTIFY = "spotify",
  YT_MUSIC = "ytmusic",
}

// TODO maybe model this as Provider objects?
const ProviderData = new Map([
  [Provider.SPOTIFY, { display_name: "Spotify" }],
  [Provider.YT_MUSIC, { display_name: "YouTube Music" }],
]);

interface Playlist {
  id: string;
  name: string;
  is_liked: boolean;
}

export { Provider, ProviderData, Playlist };
