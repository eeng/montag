import { useEffect, useState } from "react";
import { api } from "../api";
import { Playlist, Provider, ProviderData } from "../domain";
import { PlaylistItem } from "./PlaylistItem";

type Props = {
  provider?: Provider;
  onSelect(playlist: Playlist): void;
};

export const PlaylistList = ({ provider, onSelect }: Props) => {
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
      {playlists &&
        playlists.map((playlist) => (
          <PlaylistItem
            key={playlist.id}
            playlist={playlist}
            onSelect={onSelect}
          />
        ))}
    </div>
  );
};
