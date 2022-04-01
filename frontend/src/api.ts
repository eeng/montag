import { Playlist, Provider } from "./domain";

interface MeResponse {
  authorized_providers: Provider[];
}

interface PlaylistsResponse {
  playlists: Playlist[];
}

interface Api {
  me(): Promise<MeResponse>;
  playlists(provider: Provider): Promise<PlaylistsResponse>;
}

export const api: Api = {
  me: () =>
    fetch("/api/me").then((response) =>
      response.json().then((json) => json["data"])
    ),
  playlists: (provider) =>
    fetch(`/api/playlists?provider=${provider}`).then((response) =>
      response.json().then((json) => json["data"])
    ),
};
