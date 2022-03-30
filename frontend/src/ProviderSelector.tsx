import { Provider } from "./domain";

type Props = {
  onSelect: (provider: Provider) => void;
};

export const ProviderSelector = ({ onSelect }: Props) => (
  <div>
    <button onClick={() => onSelect(Provider.SPOTIFY)}>Spotify</button>
    <button onClick={() => onSelect(Provider.YTMUSIC)}>YouTube Music</button>
  </div>
);
