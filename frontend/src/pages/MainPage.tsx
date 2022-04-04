import { Provider } from "../domain";
import { PlaylistList } from "../components/PlaylistList";
import { ProviderSelector } from "../components/ProviderSelector";
import { useSession } from "../contexts/SessionContext";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function MainPage() {
  const { isAuthorized } = useSession();
  const navigate = useNavigate();
  const [srcProvider, setSrcProvider] = useState<Provider>();

  const requestAuthorization = (provider: Provider) =>
    navigate(`/auth/${provider}`);

  const onSrcProviderSelected = (provider: Provider) => {
    if (isAuthorized(provider)) setSrcProvider(provider);
    else requestAuthorization(provider);
  };

  const onReset = () => setSrcProvider(undefined);

  return (
    <div>
      <button onClick={onReset}>Reset</button>
      <p>Where would you like to migrate your music from?</p>
      <ProviderSelector onSelect={onSrcProviderSelected} />
      <PlaylistList provider={srcProvider} onSelect={console.log} />
    </div>
  );
}
