import { ProviderSelector } from "./ProviderSelector";

export function App() {
  return (
    <div>
      <p>Where would you like to migrate your music from?</p>
      <ProviderSelector onSelect={console.log} />
    </div>
  );
}
