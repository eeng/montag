import { Provider, Providers } from "../domain";

type Props = {
  onSelect: (provider: Provider) => void;
};

export const ProviderSelector = ({ onSelect }: Props) => (
  <div>
    {Providers.map((provider) => (
      <button key={provider.id} onClick={() => onSelect(provider)}>
        {provider.displayName}
      </button>
    ))}
  </div>
);
