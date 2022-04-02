import { useEffect, useState } from "react";
import { api } from "../api";
import { Playlist, Provider } from "../domain";

type Props = {
  provider?: Provider;
};

export const PlaylistList = ({ provider }: Props) => {
  if (!provider) return null;

  const [playlists, setPlaylists] = useState<Playlist[]>();

  useEffect(() => {
    api.playlists(provider).then(setPlaylists);
  }, [provider]);

  return (
    <div>
      <p>{provider} Playlists</p>
      {!playlists && "Loading..."}
      {playlists && JSON.stringify(playlists)}
    </div>
  );
};
