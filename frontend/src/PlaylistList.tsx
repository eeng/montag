import { api } from "./api";
import { Provider } from "./domain";

type Props = {
  provider: Provider;
};

export const PlaylistList = ({ provider }: Props) => {
  const fetchPlaylists = () => {
    api.playlists(provider).then((data) => console.log(data));
  };

  return (
    <div>
      <p>Playlists</p>
      <button onClick={fetchPlaylists}>Fetch</button>
    </div>
  );
};
