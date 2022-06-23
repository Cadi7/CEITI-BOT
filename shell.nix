{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
  buildInputs = [
    python39Full
    python39Packages.discordpy
    python39Packages.beautifulsoup4
    python39Packages.requests
  ];
}
