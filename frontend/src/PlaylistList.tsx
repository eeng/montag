import { Provider } from "./domain";

type Props = {
  provider: Provider;
};

export const PlaylistList = ({ provider }: Props) => {
  const fetchPlaylists = () => {
    fetch(`/api/playlists?provider=${provider}`)
      .then((response) => response.json())
      .then((data) => console.log(data));
  };

  return (
    <div>
      <p>Playlists</p>
      <button onClick={fetchPlaylists}>Fetch</button>
    </div>
  );
};
