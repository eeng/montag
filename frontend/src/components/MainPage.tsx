import { Provider } from "../domain";
import { PlaylistList } from "../components/PlaylistList";
import { ProviderSelector } from "../components/ProviderSelector";
import { useSession } from "../contexts/SessionContext";

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

export function MainPage() {
  const { isAuthorized } = useSession();
  console.log(isAuthorized(Provider.SPOTIFY));
  return (
    <div>
      <p>Where would you like to migrate your music from?</p>
      <ProviderSelector onSelect={handleProviderSelected} />
      <PlaylistList provider={Provider.SPOTIFY} />
    </div>
  );
}
