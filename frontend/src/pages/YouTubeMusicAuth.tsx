export function YouTubeMusicAuth() {
  return (
    <div>
      <div>Let's connect your YouTube Music account</div>
      <div>Paste your YouTube Music headers here:</div>
      <form
        action={`/ytmusic/login?return_to=${location.origin}`}
        method="POST"
      >
        <textarea name="headers_raw" rows={10} cols={80} />
        <button type="submit">Connect</button>
      </form>
    </div>
  );
}
