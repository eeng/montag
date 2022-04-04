import { Playlist, ProviderId } from "./domain";

interface MeResponse {
  authorized_providers: ProviderId[];
}

interface Api {
  me(): Promise<MeResponse>;
  playlists(provider: ProviderId): Promise<Playlist[]>;
}

const request = (url: string) =>
  fetch(url)
    .then((response) => response.json())
    .then((json) => json["data"]);

export const api: Api = {
  me: () => request("/api/me"),
  playlists: (provider) => request(`/api/playlists?provider=${provider}`),
};
