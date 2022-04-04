import { useEffect, useState } from "react";
import { api } from "../api";
import { Playlist, Provider, ProviderData } from "../domain";

type Props = {
  provider?: Provider;
};

export const PlaylistList = ({ provider }: Props) => {
  if (!provider) return null;

  const [playlists, setPlaylists] = useState<Playlist[]>();

  useEffect(() => {
    setPlaylists(undefined);
    api.playlists(provider).then(setPlaylists);
  }, [provider]);

  return (
    <div>
      <p>{ProviderData.get(provider).display_name} Playlists</p>
      {!playlists && "Loading..."}
      {playlists && JSON.stringify(playlists)}
    </div>
  );
};
