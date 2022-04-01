import { Playlist, Provider } from "./domain";

interface MeResponse {
  authorized_providers: Provider[];
}

interface Api {
  me(): Promise<MeResponse>;
  playlists(provider: Provider): Promise<Playlist[]>;
}

const request = (url: string) =>
  fetch(url)
    .then((response) => response.json())
    .then((json) => json["data"]);

export const api: Api = {
  me: () => request("/api/me"),
  playlists: (provider) => request(`/api/playlists?provider=${provider}`),
};
