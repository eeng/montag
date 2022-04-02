export function SpotifyAuth() {
  function connect() {
    const return_to = location.origin;
    location.href = `/spotify/login?return_to=${return_to}`;
  }

  return (
    <div>
      <p>Let's connect your Spotify account</p>
      <button onClick={connect}>Connect</button>
    </div>
  );
}
