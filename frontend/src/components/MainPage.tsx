import { Provider } from "../domain";
import { PlaylistList } from "../components/PlaylistList";
import { ProviderSelector } from "../components/ProviderSelector";
import { useSession } from "../contexts/SessionContext";
import { useState } from "react";

function startAuthFlow(provider: Provider) {
  switch (provider) {
    case Provider.SPOTIFY:
      const return_to = location.href;
      location.href = `/spotify/login?return_to=${return_to}`;
      break;

    default:
      break;
  }
}

export function MainPage() {
  const { isAuthorized } = useSession();
  const [srcProvider, setSrcProvider] = useState<Provider>();

  const onSrcProviderSelected = (provider: Provider) => {
    if (isAuthorized(provider)) setSrcProvider(provider);
    else startAuthFlow(provider);
  };

  const onReset = () => setSrcProvider(undefined);

  return (
    <div>
      <button onClick={onReset}>Reset</button>
      <p>Where would you like to migrate your music from?</p>
      <ProviderSelector onSelect={onSrcProviderSelected} />
      <PlaylistList provider={srcProvider} />
    </div>
  );
}
