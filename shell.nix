with import <nixpkgs> {};

mkShell {
  buildInputs = [
    python3
    poetry
  ];

  POETRY_VIRTUALENVS_IN_PROJECT = true;
}