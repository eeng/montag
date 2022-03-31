import { Provider } from "./domain";
import { PlaylistList } from "./PlaylistList";
import { ProviderSelector } from "./ProviderSelector";
import { api } from "./api";

const handleProviderSelected = (provider: Provider) => {
  switch (provider) {
    case Provider.SPOTIFY:
      const backend_url = "http://localhost:5000";
      const return_to = location.href;
      location.href = `${backend_url}/spotify/login?return_to=${return_to}`;
      break;

    default:
      break;
  }
};

export function App() {
  return (
    <div>
      <p>Where would you like to migrate your music from?</p>
      <ProviderSelector onSelect={handleProviderSelected} />
      <PlaylistList provider={Provider.SPOTIFY} />
      <button onClick={() => api.me().then(console.log)}>ME</button>
    </div>
  );
}
