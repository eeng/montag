import { Playlist } from "../domain";

type Props = {
  playlist: Playlist;
  onSelect: (playlist: Playlist) => void;
};

export const PlaylistItem = ({ playlist, onSelect }: Props) => (
  <div onClick={() => onSelect(playlist)}>{playlist.name}</div>
);
