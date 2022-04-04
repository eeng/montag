import { Provider, ProviderData } from "../domain";

type Props = {
  onSelect: (provider: Provider) => void;
};

export const ProviderSelector = ({ onSelect }: Props) => (
  <div>
    {[...ProviderData].map(([provider, { display_name }]) => (
      <button onClick={() => onSelect(provider)}>{display_name}</button>
    ))}
  </div>
);
