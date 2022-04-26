import { createContext, useContext, useEffect, useState } from "react";
import { api } from "../api";
import { Provider } from "../domain";

interface Session {
  isAuthorized(provider: Provider): boolean;
}

const DEFAULT_SESSION: Session = {
  isAuthorized: (_) => false,
};

const SessionContext = createContext(DEFAULT_SESSION);

type Props = {
  children: JSX.Element;
};

export const SessionProvider = ({ children }: Props) => {
  const [session, setSession] = useState(DEFAULT_SESSION);

  useEffect(() => {
    api.me().then((response) => {
      const isAuthorized = (provider: Provider) =>
        response.authorized_providers.includes(provider.id);
      setSession({ isAuthorized });
    });
  }, []);

  return (
    <SessionContext.Provider value={session}>
      {children}
    </SessionContext.Provider>
  );
};

export const useSession = () => useContext(SessionContext);
