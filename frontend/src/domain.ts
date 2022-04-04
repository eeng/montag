export enum ProviderId {
  SPOTIFY = "spotify",
  YT_MUSIC = "ytmusic",
}

export interface Provider {
  id: ProviderId;
  displayName: string;
}

export const Providers: Provider[] = [
  { id: ProviderId.SPOTIFY, displayName: "Spotify" },
  { id: ProviderId.YT_MUSIC, displayName: "YouTube Music" },
];

export interface Playlist {
  id: string;
  name: string;
  is_liked: boolean;
}
