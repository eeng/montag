import { MainPage } from "./components/MainPage";
import { SessionProvider } from "./contexts/SessionContext";

export const App = () => (
  <SessionProvider>
    <MainPage />
  </SessionProvider>
);
