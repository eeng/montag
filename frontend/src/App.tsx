import { BrowserRouter, Route, Routes } from "react-router-dom";
import { MainPage } from "./pages/MainPage";
import { SessionProvider } from "./contexts/SessionContext";
import { SpotifyAuth } from "./pages/SpotifyAuth";
import { YouTubeMusicAuth } from "./pages/YouTubeMusicAuth";

export const App = () => (
  <SessionProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/auth/spotify" element={<SpotifyAuth />} />
        <Route path="/auth/ytmusic" element={<YouTubeMusicAuth />} />
      </Routes>
    </BrowserRouter>
  </SessionProvider>
);
